# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Module that handles running tests on Docker image"""
import logging
import pathlib
import typing

from docker.errors import APIError, ImageNotFound
from docker.models.containers import Container
from docker.models.images import Image

from utils import logger
from utils.docker_api import DockerAPI
from utils.exceptions import FailedTestError
from utils.utilities import get_system_proxy

log = logging.getLogger('docker_ci')


class DockerImageTesterBase(DockerAPI):
    """Wrapper for docker.api.client implementing custom docker.image.run execution and logging"""

    def __init__(self, registry=''):
        super().__init__()
        self.container: typing.Optional[Container] = None
        self.registry = registry
        log.setLevel(logging.DEBUG)

    def stop(self):
        """Stop the container"""
        if self.container:
            self.container.stop()

    def _get_logfile_path(self, image_tag, name):
        """Get path to logfile for specified test name"""
        file_tag = image_tag.replace('/', '_').replace(':', '_')
        return pathlib.Path(self.location) / 'logs' / file_tag / f'{name}.log'

    def _exec_and_log_output(self, commands: typing.List[str], logfile: pathlib.Path, prefix: str):
        """Run specified commands in the container and write output to the log"""
        if not self.container:
            raise FailedTestError(f'{prefix}: container is not running before commands execution')
        output_total = []
        for command in commands:
            output_total.append(f'    === executing command: {command} ===')
            exit_code, output = self.container.exec_run(cmd=command)
            output_total.append(output.decode('utf-8'))
            if exit_code != 0:
                log.error(f'- {prefix}: command {command} have returned non-zero exit code {exit_code}')
                log.error(f'Failed command stdout: {output_total[-1]}')
                logger.switch_to_custom(logfile, str(logfile.parent))
                for output in output_total:
                    log.error(str(output))
                logger.switch_to_summary()
                raise FailedTestError(f'{prefix}: command {command} '
                                      f'have returned non-zero exit code {exit_code}')
            self.container.reload()
            if self.container.status != 'running':
                raise FailedTestError(f'{prefix}: command exit code is 0, '
                                      'but container status != "running" after this command')
        logger.switch_to_custom(logfile, str(logfile.parent))
        for output in output_total:
            log.info(str(output))
        logger.switch_to_summary()

    def __del__(self):
        """Custom __del__ to manually stop (but not remove) testing container"""
        self.stop()
        super().__del__()


class DockerImageTester(DockerImageTesterBase):
    def __init__(self, registry=''):
        super().__init__(registry)

    def test_docker_image(self,
                          image: typing.Tuple[Image, str],
                          commands: typing.List[str], test_name: str,
                          is_cached: bool = False, **kwargs: typing.Optional[typing.Dict]):
        """Running list of commands inside the container, logging the output and handling possible exceptions"""
        if isinstance(image, Image):
            image_tag = image.tags[0]
        elif isinstance(image, str):
            image_tag = image
        else:
            raise FailedTestError(f'{image} is not a proper image, must be of "str" or "docker.models.images.Image"')
        logfile = self._get_logfile_path(image_tag, test_name)

        run_kwargs = {'auto_remove': True,
                      'detach': True,
                      'use_config_proxy': True,
                      'environment': get_system_proxy(),
                      'stdin_open': True,
                      'tty': True,
                      'user': 'root'}
        if kwargs is not None:
            run_kwargs.update(kwargs)

        try:
            if self.container and image not in self.container.image.tags:
                self.container.stop()
                self.container = None
            if self.container and not is_cached:
                self.container.stop()
            if not self.container or not is_cached:
                try:
                    self.client.images.get(image_tag)
                except ImageNotFound:
                    image_tag_full = f'{self.registry}{"/" if self.registry else ""}{image_tag}'
                    log.warning(f'Image {image_tag_full} not found. Trying to pull it...')
                    self.client.images.pull(image_tag_full)
                    self.client.images.get(image_tag_full).tag(image_tag)
                self.container = self.client.containers.run(image=image, **run_kwargs)
        except APIError as err:
            raise FailedTestError(f'Docker daemon API error while starting the container: {err}')

        if not self.container:
            raise FailedTestError('Cannot create/start the container')

        try:
            self._exec_and_log_output(commands, logfile, f'Test {test_name}')
        except APIError as err:
            raise FailedTestError(f'Docker daemon API error while executing test {test_name}: {err}')


class DockerImageTesterSharedContainer(DockerImageTesterBase):
    def __init__(self, image, container_name, init_commands: typing.List[str], registry='',
                 **init_kwargs: typing.Optional[typing.Dict]):
        super().__init__(registry)

        if isinstance(image, Image):
            image_tag = image.tags[0]
        elif isinstance(image, str):
            image_tag = image
        else:
            raise FailedTestError(f'{image} is not a proper image, must be of "str" or "docker.models.images.Image"')

        self.container_name: str = container_name
        self.image_tag: str = image_tag

        logfile = self._get_logfile_path(self.image_tag, container_name)

        run_kwargs = {'auto_remove': True,
                      'detach': True,
                      'use_config_proxy': True,
                      'environment': get_system_proxy(),
                      'mem_limit': '4g',
                      'stdin_open': True,
                      'tty': True,
                      'user': 'root'}
        if init_kwargs is not None:
            run_kwargs.update(init_kwargs)

        try:
            self.container = self.client.containers.run(image=image, **run_kwargs)
        except APIError as err:
            raise FailedTestError(f'Docker daemon API error while starting the container: {err}')
        if not self.container:
            raise FailedTestError('Cannot create/start the container')

        try:
            self._exec_and_log_output(init_commands, logfile, f'Init {container_name}')
        except APIError as err:
            raise FailedTestError(f'Docker daemon API error while initializing container {container_name}: {err}')

    def run_test(self, commands: typing.List[str], test_name: str):
        """Running list of commands inside the container, logging the output and handling possible exceptions"""

        logfile = self._get_logfile_path(self.image_tag, test_name)

        if not self.container:
            raise FailedTestError('The container is not running')

        try:
            self._exec_and_log_output(commands, logfile, f'Test {test_name}')
        except APIError as err:
            raise FailedTestError(f'Docker daemon API error while executing test {test_name}: {err}')
