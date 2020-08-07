#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Main script of this framework, putting all the logic together"""
import argparse
import enum
import logging
import os
import pathlib
import platform
import shutil
import sys
import timeit
import traceback
import typing

import pytest  # noqa: I001
from docker.errors import APIError, ImageNotFound
from docker.models.images import Image
from pytest import ExitCode as PytestExitCode

from utils import logger
from utils.arg_parser import parse_args
from utils.builder import DockerImageBuilder
from utils.docker_api import DockerAPI
from utils.exceptions import (FailedBuild, FailedDeploy,  # noqa: I001
                              FailedSave, FailedStep, FailedTest)
from utils.loader import INTEL_OCL_RELEASE
from utils.render import DockerFileRender
from utils.tester import ProxyTestPlugin
from utils.utilities import download_file, format_timedelta, get_system_proxy

__version__ = '0.1'
log = logging.getLogger('project')


@enum.unique
class ExitCode(enum.Enum):
    """Enum that handles framework-specific exitcodes"""
    success = 0
    failed = 10
    failed_build = 11
    failed_test = 12
    failed_deploy = 13
    failed_save = 14
    interrupted = 130
    wrong_args = 127


class Launcher:
    """Main class implementing high-end framework logic"""

    def __init__(self, product: str, arguments: argparse.Namespace):
        self.render: typing.Optional[DockerFileRender] = None
        self.builder: typing.Optional[DockerImageBuilder] = None
        self.product_name = product
        self.args = arguments
        self.image: typing.Optional[Image] = None
        self.image_name = arguments.tags[0]
        self.kwargs: typing.Dict[str, str] = {}
        self.location = pathlib.Path(os.path.realpath(__file__)).parent
        self.mount_root: pathlib.Path = self.location / 'tests' / 'tmp' / 'mount'
        self.proxy_plugin = ProxyTestPlugin(self.args)
        self.docker_api: typing.Optional[DockerAPI] = None
        self.logdir: pathlib.Path = self.location / 'logs' / str(self.image_name).replace('/', '_').replace(':', '_')

    def set_docker_api(self):
        """Setting up Docker Python API client"""
        self.docker_api = DockerAPI()

    def setup_build_args(self):
        """Setting up arguments passed to `docker build` command"""
        self.kwargs.update({
            'name': self.product_name,
            'package_url': self.args.package_url,
            'build_id': self.args.build_id,
            'distribution': self.args.distribution,
        })
        if self.args.proxy:
            self.kwargs.update(self.args.proxy)
        else:
            self.kwargs.update(get_system_proxy())

        self.kwargs.update(INTEL_OCL_RELEASE[self.args.ocl_release])

        if self.args.build_arg:
            for arg in self.args.build_arg:
                self.kwargs.update({arg.split('=')[0]: arg.split('=')[-1]})

    def generate_docker_file(self):
        """Generating dockerfile based on templates and CLI options"""
        log.info('Preparing to generate the dockerfile...')
        self.render = DockerFileRender(self.args.os)
        self.args.file = self.render.generate_dockerfile(self.args, self.kwargs)
        if 'hadolint' in self.args.linter_check:
            log.info(logger.LINE_DOUBLE)
            log.info('Running linter checks on the generated dockerfile...')
            handolint_report = self.logdir / 'dockerfile_linter_hadolint.html'
            result = pytest.main(args=[f'{self.location / "tests" / "linters"}', '-k', 'hadolint',
                                       '--dockerfile', str(self.args.file),
                                       f'--junitxml={self.logdir / "hadolint.xml"}',
                                       f'--html={handolint_report}',
                                       '--self-contained-html', '--tb=no', '--color=yes'],
                                 plugins=[self.proxy_plugin])
            if result == PytestExitCode.OK:
                log.info('Linter checks: PASSED')
            else:
                log.warning('Linter checks: FAILED')
            log.info(f'Hadolint report location: {handolint_report}')

    def build(self):
        """Building Docker image from dockerfile"""
        log.info(logger.LINE_DOUBLE)
        log.info('Preparing to build Docker image...')
        tmp_folder, self.args.old_package_url = '', ''

        if self.args.source == 'local' and self.args.package_url.startswith(('http://', 'https://', 'ftp://')):
            log.info('Downloading needed files...')
            self.args.old_package_url = self.args.package_url
            archive_name = self.args.old_package_url.split('/')[-1]
            tmp_folder = self.location / 'tmp'

            download_file(str(self.args.package_url), tmp_folder / archive_name, proxy=self.args.proxy,
                          parents_=True)

            self.args.package_url = (tmp_folder / archive_name).relative_to(self.location)
            self.args.package_url = str(pathlib.PurePosixPath(self.args.package_url))
            log.info('Downloading finished')
        self.kwargs['package_url'] = self.args.package_url

        log.info('Building Docker image...')
        if not self.args.path:
            self.args.path = self.location
        else:
            self.args.path = pathlib.Path(self.args.path)
        self.args.file = pathlib.Path(self.args.file)
        if self.args.file.is_absolute():
            self.args.file = pathlib.Path(self.args.file).relative_to(self.args.path)
        self.builder = DockerImageBuilder()
        curr_time = timeit.default_timer()
        self.image = self.builder.build_docker_image(dockerfile=self.args.file,
                                                     directory=str(self.args.path),
                                                     tag=self.image_name,
                                                     build_args=self.kwargs,
                                                     logfile=self.logdir / 'image_build.log')
        log.info(f'Build time: {format_timedelta(timeit.default_timer() - curr_time)}')
        log.info(f"Build log location: {self.logdir / 'image_build.log'}")
        if not self.image:
            raise FailedBuild(f'Error building Docker image {self.args.tags}')
        log.info(f'Docker image {self.args.tags} built successfully')

        if self.args.old_package_url != '':
            self.args.package_url, self.args.old_package_url = self.args.old_package_url, self.args.package_url
            self.kwargs['package_url'] = self.args.package_url
        if tmp_folder != '' and tmp_folder.exists():
            shutil.rmtree(tmp_folder)
        log.info('Build dependencies deleted')

    def dive_linter_check(self):
        """Checking the Docker image size optimality using the Dive tool (https://github.com/wagoodman/dive)"""
        log.info(logger.LINE_DOUBLE)
        log.info('Running dive checks on the docker image...')
        log.info('This may take some time for big image...')
        dive_report = self.logdir / 'image_linter_dive.html'
        curr_time = timeit.default_timer()
        result = pytest.main(args=[f'{self.location / "tests" / "linters"}', '-k', 'dive', '--image',
                                   self.image_name,
                                   f'--junitxml={self.logdir / "dive.xml"}',
                                   f'--html={dive_report}',
                                   '--self-contained-html', '--tb=no', '--color=yes'],
                             plugins=[self.proxy_plugin])
        log.info(f'Testing time: {format_timedelta(timeit.default_timer() - curr_time)}')
        if result == PytestExitCode.OK:
            log.info('Dive checks: PASSED')
        else:
            log.warning('Dive image checks: FAILED')
        log.info(f'Dive report location: {dive_report}')

    def sdl_check(self):
        """Checking the Docker image security

        Learn more:
        * docker-bench-security (https://github.com/docker/docker-bench-security)
        * Snyk (https://snyk.io/product/container-vulnerability-management/)
        """
        log.info(logger.LINE_DOUBLE)
        log.info('Running SDL checks on host and the image...')
        sdl_report = str(self.logdir / 'sdl.html')
        curr_time = timeit.default_timer()
        sdl_check = ' or '.join(self.args.sdl_check)
        result = pytest.main(args=[f'{self.location / "tests" / "security"}', '-k', sdl_check,
                                   '--image', self.image_name,
                                   f'--junitxml={self.logdir / "sdl.xml"}',
                                   f'--html={sdl_report}',
                                   '--self-contained-html', '--tb=no', '--color=yes'],
                             plugins=[self.proxy_plugin])
        log.info(f'Testing time: {format_timedelta(timeit.default_timer() - curr_time)}')
        if result == PytestExitCode.OK:
            log.info('SDL checks: PASSED')
        else:
            log.warning('SDL checks: FAILED')
        log.info(f'SDL report location: {sdl_report}')

    def test(self):
        """Run pytest-based tests on the built Docker image"""
        log.info(logger.LINE_DOUBLE)
        log.info(f'Preparing to run tests on the Docker image {self.image_name}...')
        if self.args.sdl_check:
            self.sdl_check()
        if 'dive' in self.args.linter_check:
            self.dive_linter_check()
        test_report = self.logdir / 'tests.html'
        curr_time = timeit.default_timer()
        test_expression = ''
        if self.args.test_expression:
            test_expression = self.args.test_expression
        result = pytest.main([f'{self.location / "tests" / "functional"}', '-k', test_expression,
                              '--image', self.image_name,
                              '--distribution', self.args.distribution,
                              '--image_os', self.args.os,
                              '--mount_root', str(self.mount_root),
                              # package_url is now mandatory for test-only runtime testing
                              '--package_url', self.args.package_url,
                              f"--junitxml={self.logdir / 'tests.xml'}",
                              f'--html={test_report}',
                              '--self-contained-html', '--tb=no', '--color=yes'])
        log.info(f'Testing time: {format_timedelta(timeit.default_timer() - curr_time)}')
        if result == PytestExitCode.OK:
            log.info('Tests: PASSED')
            log.info(f'Testing report location: {test_report}')
            log.info(f'Testing detailed logs location: {test_report.parent}')
        else:
            log.error('Tests: FAILED')
            log.info(f'Testing report location: {test_report}')
            log.info(f'Testing detailed logs location: {test_report.parent}')
            raise FailedTest('Tests failed')

    def tag(self):
        """Tag built Docker image"""
        log.info(logger.LINE_DOUBLE)
        log.info('Tagging built Docker image...')
        try:
            for tag in self.args.tags:
                if self.args.registry not in self.image_name:
                    is_passed = self.docker_api.client.images.get(self.image_name).tag(
                        self.args.registry + '/' + tag)
                    if not is_passed:
                        raise FailedDeploy(f"Can't tag {self.image_name} image to {self.args.registry}/{tag}")
                    log.info(f'Image {self.image_name} successfully tagged as {self.args.registry}/{tag}')
        except ImageNotFound as err:
            raise FailedDeploy(f'{err}')
        except APIError as err:
            raise FailedDeploy(f'Tagging failed: {err}')

    def deploy(self):
        """Push built Docker image to repo specified in CLI"""
        log.info(logger.LINE_DOUBLE)
        log.info('Publishing built Docker image...')
        try:
            curr_time = timeit.default_timer()
            for tag in self.args.tags:
                if self.args.registry in tag:
                    log_generator = self.docker_api.client.images.push(tag,
                                                                       stream=True, decode=True)
                else:
                    log_generator = self.docker_api.client.images.push(self.args.registry + '/' + tag,
                                                                       stream=True, decode=True)
                log.info(f'Push time: {format_timedelta(timeit.default_timer() - curr_time)}')
                log_name = f'deploy_{tag.replace("/", "_").replace(":", "_")}.log'
                log_path_file = self.logdir / log_name
                log.info(f'Image {tag} push log location: {log_path_file}')
                logger.switch_to_custom(log_name)
                for line in log_generator:
                    for key, value in line.items():
                        if 'error' in key or 'errorDetail' in key:
                            log.error(f'{value}')
                            raise FailedDeploy(f'{value}')
                        log.info(f'{value}')
                logger.switch_to_summary()
                log.info('Image successfully published')
        except APIError as err:
            raise FailedDeploy(f'Push had failed: {err}')

    def save(self):
        """Save Docker image as a local binary file"""
        log.info(logger.LINE_DOUBLE)
        log.info('Saving built Docker image...')
        curr_time = timeit.default_timer()
        share_root = pathlib.Path(self.args.nightly_save_path)
        archive_name = ''
        for tag in self.args.tags:
            if not tag.endswith('latest'):
                tag = tag.split('/')[-1]  # remove registry from tag
                archive_name = f'{tag.replace(":", "_")}.bin'
                break
        try:
            if not self.image:
                self.image = self.docker_api.client.images.get(self.args.tags[0])
            with open(share_root / archive_name, 'wb') as file:
                for chunk in self.image.save(chunk_size=None):
                    file.write(chunk)
            log.info(f'Save time: {format_timedelta(timeit.default_timer() - curr_time)}')
        except (PermissionError, FileExistsError, FileNotFoundError) as file_err:
            raise FailedSave(f'Saving the image was failed due to file-related error: {file_err}')
        except APIError as err:
            raise FailedSave(f'Saving the image was failed: {err}')

    def rmi(self):
        """Remove Docker image from the host machine"""
        self.docker_api.client.images.remove(self.image_name, force=True)


if __name__ == '__main__':
    started_time = timeit.default_timer()
    exit_code = ExitCode.success
    try:
        logfile = logger.init_logger()
        product_name = 'Intel(R) Distribution of OpenVINO(TM) toolkit'
        des = f'DockerHub CI framework for {product_name}'
        args = parse_args(name=os.path.basename(__file__), description=des)
        launcher = Launcher(product_name, args)

        log.info(logger.LINE_DOUBLE)
        log.info(f'{des} v{__version__}')
        log.info(logger.LINE_DOUBLE)
        log.info(f'Log:         {logfile}')
        log.info(f'Command:     {" ".join(sys.argv)}')
        log.info(f'Machine:     {platform.node()}')
        log.info(f'System:      {platform.system().lower()}; {platform.release()}; {platform.machine()}')
        log.info(f'Python:      "{sys.executable}" {sys.version}')
        log.info(logger.LINE_DOUBLE)

        if args.mode == 'deploy':
            launcher.set_docker_api()
            launcher.tag()
            launcher.deploy()
            if args.nightly_save_path:
                launcher.save()

        if args.mode == 'gen_dockerfile':
            launcher.setup_build_args()
            launcher.generate_docker_file()

        if args.mode == 'build':
            launcher.set_docker_api()
            launcher.setup_build_args()
            if not args.file:
                launcher.generate_docker_file()
            launcher.build()

        if args.mode == 'build_test':
            launcher.set_docker_api()
            launcher.setup_build_args()
            if not args.file:
                launcher.generate_docker_file()
            launcher.build()
            launcher.test()

        if args.mode == 'test':
            launcher.test()

        if args.mode == 'all':
            launcher.set_docker_api()
            launcher.setup_build_args()
            if not args.file:
                launcher.generate_docker_file()
            launcher.build()
            if not args.nightly:
                launcher.test()
            launcher.tag()
            launcher.deploy()
            if args.nightly_save_path:
                launcher.save()
            if args.nightly:
                launcher.test()
                launcher.rmi()  # doesn't check anything here because any error before this step should `raise` itself

    except FailedStep as error:
        logger.switch_to_summary()
        log.error(f'{error}')
        exit_code = ExitCode.failed
    except FailedBuild as error:
        logger.switch_to_summary()
        log.error(f'{error}')
        exit_code = ExitCode.failed_build
    except FailedTest as error:
        logger.switch_to_summary()
        log.error(f'{error}')
        exit_code = ExitCode.failed_test
    except FailedDeploy as error:
        logger.switch_to_summary()
        log.error(f'{error}')
        exit_code = ExitCode.failed_deploy
    except FailedSave as error:
        logger.switch_to_summary()
        log.error(f'{error}')
        exit_code = ExitCode.failed_save
    except KeyboardInterrupt:
        logger.switch_to_summary()
        log.info(logger.LINE_SINGLE)
        log.error(f'{__file__} was interrupted')
        log.info(logger.LINE_SINGLE)
        exit_code = ExitCode.interrupted
    except SystemExit:
        sys.exit(ExitCode.wrong_args.value)
    except Exception as ex:
        logger.switch_to_summary()
        log.info(logger.LINE_SINGLE)
        log.error(f'Something goes wrong **FAILED**: {ex}')
        log.error(f'Error: {traceback.format_exc()}')
        log.info(logger.LINE_SINGLE)
        exit_code = ExitCode.failed
    log.info(logger.LINE_DOUBLE)
    log.info(f'Total time elapsed: {format_timedelta(timeit.default_timer() - started_time)}')
    log.info(f'Exit code: {exit_code.value}')

    sys.exit(exit_code.value)
