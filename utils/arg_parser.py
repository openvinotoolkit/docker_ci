# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""CLI arguments parser for this framework"""
import argparse
import contextlib
import pathlib
import re
import subprocess  # nosec
import sys
import typing
import logging

from utils.loader import INTEL_OPENVINO_VERSION
from utils.utilities import (check_internal_local_path,
                             check_printable_utf8_chars)

logger = logging.getLogger(__name__)


class DockerCIArgumentParser(argparse.ArgumentParser):
    """CLI argument parser for this framework"""

    SUPPORTED_OS: typing.List = ['ubuntu18', 'ubuntu20', 'ubuntu22','winserver2019', 'windows20h2', 'rhel8']

    def __init__(self, prog: typing.Optional[str] = None, description: typing.Optional[str] = None):
        super().__init__(prog=prog, description=description,
                         formatter_class=argparse.RawTextHelpFormatter, add_help=True)

    @staticmethod
    def set_default_subparser(name: str):
        """Set default subparser"""
        if not sys.argv[1:]:
            sys.argv.insert(1, name)

    @staticmethod
    def add_image_args(parser: argparse.ArgumentParser):
        """Adding args needed to manage the built Docker image"""
        parser.add_argument(
            '-t',
            '--tags',
            metavar='IMAGE_NAME:TAG',
            action='append',
            required=' test' in parser.prog,
            help='Source image name and optionally a tags in the "IMAGE_NAME:TAG" format. '
                 'Default is <os>_<distribution>:<product_version> and latest. You can specify some tags.',
        )

        parser.add_argument(
            '--tag_postfix',
            metavar='_NAME',
            default='',
            help='Add special postfix to the end of tag image. '
                 'Image name will be like this <os>_<distribution>:<product_version><tag_postfix>',
        )

    @staticmethod
    def add_linter_check_args(parser: argparse.ArgumentParser):
        parser.add_argument(
            '--linter_check',
            metavar='NAME',
            action='append',
            default=[],
            help='Enable linter check for image and dockerfile. '
                 'It installs additional 3d-party docker images or executable files. '
                 'Available tests: '
                 'hadolint (https://github.com/hadolint/hadolint), '
                 'dive (https://github.com/wagoodman/dive)',
        )

    @staticmethod
    def add_build_args(parser: argparse.ArgumentParser):
        """Adding args needed to build the Docker image"""
        parser.add_argument(
            '--wheels_url',
            metavar='URL',
            default='',
            help='URL to HTML page with links or local path relative to openvino folder to search for OpenVINO wheels '
                 '(will be used in a dockerfile as pip install --find-links value). '
                 'By default, openvino and openvino_dev will be installed from PyPi',
        )

        parser.add_argument(
            '--image_json_path',
            help='Provide path to save image data in .json format file. '
                 'By default, it is stored in the logs folder.')

        parser.add_argument(
            '--dockerfile_name',
            metavar='NAME',
            help='Name of the Dockerfile, that will be generated from templates. '
                 'Format is "openvino_<devices>_<distribution>_<product_version>.dockerfile"',
        )

        parser.add_argument(
            '-d',
            '--device',
            metavar='NAME',
            action='append',
            help='Target inference hardware: cpu, gpu, vpu, hddl. Default is all. '
                 'Dockerfile name format has the first letter from device name, '
                 'e.g. for CPU, HDDL it will be openvino_ch_<distribution>_<product_version>.dockerfile',
        )

        parser.add_argument(
            '-py',
            '--python',
            choices=['python37', 'python38', 'python310'],
            help='Python interpreter for docker image, currently default is python38',
        )

        parser.add_argument(
            '--cmake',
            choices=['cmake34', 'cmake314'],
            default='cmake314',
            help='CMake for Windows docker image, default CMake 3.14. For Linux images it is used default for OS.',
        )

        parser.add_argument(
            '--msbuild',
            choices=['msbuild2019', 'msbuild2019_online'],
            help='MSBuild Tools for Windows docker image.'
                 'MSBuild Tools are licensed as a supplement your existing Visual Studio license. '
                 'Please don’t share the image with MSBuild 2019 on a public Docker Hub.',
        )

        parser.add_argument(
            '--pre_stage_msbuild',
            choices=['msbuild2019', 'msbuild2019_online'],
            help='MSBuild Tools for Windows docker image to use on the first stage. '
                 'Can be required to build some thirdparty dependencies from source code. '
                 'MSBuild Tools are licensed as a supplement your existing Visual Studio license. ',
        )

        parser.add_argument(
            '-l',
            '--layers',
            metavar='NAME',
            action='append',
            default=[],
            help='Setup your layer. Use name of <your_layer>.dockerfile.j2 file located in '
                 '<project_root>/templates/<image_os>/layers folder. '
                 'Layer will be added to the end of product dockerfile.',
        )

        parser.add_argument(
            '--build_arg',
            metavar='VAR_NAME=VALUE',
            action='append',
            default=[],
            help='Specify build or template arguments for your layer. '
                 'You can use "no_samples=True" to remove OMZ, IE samples and demos from final docker image. '
                 'Set "INSTALL_SOURCES=yes" to download source for 3d party LGPL/GPL dependencies.',
        )

        parser.add_argument(
            '--no-cache',
            dest='no_cache',
            action='store_true',
            help='Specify if image should be built without cache. False by default.',
        )

    @staticmethod
    def add_test_args(parser: argparse.ArgumentParser):
        """Adding args needed to run tests on the built Docker image"""
        parser.add_argument(
            '-k',
            metavar='EXPRESSION',
            default='',
            dest='test_expression',
            help='Run tests which match the given substring expression for pytest -k.',
        )
        parser.add_argument(
            '-m',
            metavar='MARKEXPR',
            default='',
            dest='test_mark_expression',
            help='Run tests which matching given mark expression for pytest -m',
        )

        parser.add_argument(
            '--sdl_check',
            metavar='NAME',
            action='append',
            default=[],
            help='Enable SDL check for docker host and image. '
                 'It installs additional 3d-party docker images or executable files. '
                 'Available tests: '
                 'snyk (https://github.com/snyk/snyk), '
                 'bench_security (https://github.com/docker/docker-bench-security)',
        )

        parser.add_argument(
            '--nightly',
            action='store_true',
            default=False,
            help=argparse.SUPPRESS,  # Skip tests for regular builds
        )

    @staticmethod
    def add_deploy_args(parser: argparse.ArgumentParser):
        """Adding args needed to publish the built Docker image to a repository"""
        parser.add_argument(
            '-r',
            '--registry',
            metavar='URL:PORT',
            required=True,
            help='Registry host and optionally a port in the "host:port" format',
        )

        parser.add_argument(
            '--nightly_save_path',
            default='',
            help=argparse.SUPPRESS,  # Setup saving docker image as a binary file
        )

    @classmethod
    def add_dist_args(cls, parser: argparse.ArgumentParser):
        """Adding arg needed to customize the generated dockerfile"""
        parser.add_argument(
            '-os',
            choices=cls.SUPPORTED_OS,
            default='',
            help='Operation System for docker image.',
        )

        parser.add_argument(
            '-dist',
            '--distribution',
            choices=['base', 'runtime', 'dev', 'dev_no_samples', 'custom'],
            required=' test' in parser.prog,
            help='Distribution type: dev, dev_no_samples, runtime or '
                 'base (with CPU only and without installing dependencies). '
                 'Using key --file <path_to_dockerfile> and '
                 '-p <version> are mandatory to build base distribution image.'
                 'base dockerfiles are stored in <repository_root>/dockerfiles/<os_image> folder.',
        )

        parser.add_argument('-p',
                            '--product_version',
                            default='',
                            help='Product version in format: YYYY.U[.BBB], where BBB - build number is optional.')

        parser.add_argument(
            '-w',
            '--wheels_version',
            default='',
            help='Version specifier of OpenVINO wheels to install (will be passed to pip install). '
                 'Will be equal to product version by default.',
        )

        parser.add_argument(
            '-s',
            '--source',
            choices=['url', 'local'],
            default='url',
            help='Source of the package: external URL or relative <root_project> local path. By default: url.',
        )

        parser.add_argument(
            '-u',
            '--package_url',
            metavar='URL',
            default='',
            help='Package external or local url, use http://, https://, ftp:// access scheme or '
                 'relative <root_project> local path',
        )

        parser.add_argument(
            '-f',
            '--file',
            metavar='NAME',
            help='Name of the Dockerfile, that uses to build an image.',
        )


def fail_if_product_version_not_supported(product_version: str, parser: DockerCIArgumentParser):
    if product_version < '2022.1':
        parser.error('This version of the DockerHub CI framework does not support OpenVINO releases earlier than '
                     '2022.1.0. Please use previous versions of the DockerHub CI.')

def parse_args(name: str, description: str):  # noqa
    """Parse all the args set up above"""
    parser = DockerCIArgumentParser(name, description)

    subparsers = parser.add_subparsers(dest='mode')

    gen_dockerfile_subparser = subparsers.add_parser('gen_dockerfile', help='Generate a dockerfile to '
                                                                            'dockerfiles/<image_os> folder')
    parser.add_build_args(gen_dockerfile_subparser)
    parser.add_linter_check_args(gen_dockerfile_subparser)
    parser.add_dist_args(gen_dockerfile_subparser)
    rhel_platform_group = gen_dockerfile_subparser.add_mutually_exclusive_group()
    rhel_platform_group.add_argument(
        '--rhel_platform',
        choices=['docker', 'openshift', 'autobuild'],
        default='docker',
        help='Specify target platform to generate RHEL dockerfiles (default is docker). '
             'Choose autobuild option for Red Hat portal Build System.',
    )
    rhel_platform_group.add_argument(
        '--openshift',
        action='store_const',
        dest='rhel_platform',
        const='openshift',
        default=False,
        help='Create a dockerfile intended to build on Red Hat OpenShift Container Platform (RHEL images only). '
             'Alias for --rhel_platform=openshift',
    )

    build_subparser = subparsers.add_parser('build', help='Build a docker image')
    parser.add_build_args(build_subparser)
    parser.add_linter_check_args(build_subparser)
    parser.add_dist_args(build_subparser)
    parser.add_image_args(build_subparser)

    build_test_subparser = subparsers.add_parser('build_test', help='Build and test a docker image')
    parser.add_build_args(build_test_subparser)
    parser.add_linter_check_args(build_test_subparser)
    parser.add_dist_args(build_test_subparser)
    parser.add_image_args(build_test_subparser)
    parser.add_test_args(build_test_subparser)

    test_subparser = subparsers.add_parser('test', help='Test a local docker image')
    parser.add_linter_check_args(test_subparser)
    parser.add_dist_args(test_subparser)
    parser.add_image_args(test_subparser)
    parser.add_test_args(test_subparser)
    test_subparser.add_argument(
        '-r',
        '--registry',
        metavar='URL:PORT',
        default='',
        help='Registry host and optionally a port in the "host:port" format. '
             'Will be used to pull the image if it does not exist',
    )

    deploy_subparser = subparsers.add_parser('deploy', help='Deploy a docker image')
    parser.add_image_args(deploy_subparser)
    parser.add_deploy_args(deploy_subparser)

    all_subparser = subparsers.add_parser('all', help='Build, test and deploy a docker image. [Default option]')
    parser.add_build_args(all_subparser)
    parser.add_linter_check_args(all_subparser)
    parser.add_dist_args(all_subparser)
    parser.add_image_args(all_subparser)
    parser.add_test_args(all_subparser)
    parser.add_deploy_args(all_subparser)

    parser.set_default_subparser('all')

    args = parser.parse_args()

    for key in vars(args):
        arg_val = getattr(args, key)
        if isinstance(arg_val, (list, tuple)):
            for elem in arg_val:
                check_printable_utf8_chars(elem)
        elif isinstance(arg_val, str):
            check_printable_utf8_chars(arg_val)

    for attr_name in ('package_url', 'file', 'image_json_path'):
        if hasattr(args, attr_name) and getattr(args, attr_name):
            check_internal_local_path(getattr(args, attr_name))

    if args.mode != 'deploy' and args.package_url and args.source == 'local' and not args.package_url.startswith((
            'http://', 'https://', 'ftp://')):
        args.package_url = str(pathlib.Path(args.package_url).as_posix())

    if args.mode not in ('test', 'deploy') and hasattr(args, 'distribution') and args.distribution == 'custom':
        parser.error('For a custom distribution, only test and deploy modes are available.')

    if hasattr(args, 'sdl_check') and args.sdl_check and (
            'snyk' not in args.sdl_check and 'bench_security' not in args.sdl_check):
        parser.error('Incorrect arguments for --sdl_check. Available tests: snyk, bench_security')

    if hasattr(args, 'linter_check') and args.linter_check and (
            'hadolint' not in args.linter_check and 'dive' not in args.linter_check):
        parser.error('Incorrect arguments for --linter_check. Available tests: hadolint, dive')

    if args.mode in ('build', 'build_test', 'all') and args.distribution == 'base' and not args.file:
        parser.error('The following argument is required: -f/--file')

    if args.mode == 'deploy' and not args.tags:
        parser.error('The following argument is required: -t/--tags')

    if hasattr(args, 'os') and not args.os:
        possible_os: typing.Set[str] = set()
        if args.package_url:
            possible_os.update(filter(lambda os: os in args.package_url, parser.SUPPORTED_OS))
        if hasattr(args, 'tags') and args.tags:
            for tag in args.tags:
                possible_os.update(filter(lambda os: os in tag, parser.SUPPORTED_OS))  # noqa: B023
        if len(possible_os) == 1:
            args.os = possible_os.pop()
        else:
            parser.error('Can not get image OS from package URL or tags. '
                         'Please specify -os directly')

    if args.mode in ('gen_dockerfile', 'build', 'build_test',
                     'all') and args.distribution == 'dev_no_samples' and 'ubuntu' not in args.os:
        parser.error('Distribution dev_no_samples is available only for Ubuntu operation system')

    if args.mode == 'gen_dockerfile' and args.distribution == 'base':
        parser.error('Generating dockerfile for base distribution is not available. '
                     'Use generated base dockerfiles are stored in <repository_root>/dockerfiles/<os_image> folder')

    if args.mode == 'test' and not (args.tags and args.distribution):
        parser.error('Options --tags and --distribution are mandatory. Image operation system is "ubuntu18"'
                     ' by default.')

    if args.mode == 'test' and 'runtime' in args.distribution and not args.package_url:
        logger.info('\nYou can run samples/demos on runtime docker image. '
                    'Please provide --package_url key with path to dev distribution package in '
                    'http/https/ftp access scheme or a local file in the project location as dependent package '
                    'to run all available tests.\n')

    if args.mode in ('deploy', 'all') and not hasattr(args, 'registry'):
        parser.error('Option --registry is mandatory for this mode.')

    if hasattr(args, 'image_json_path') and args.image_json_path:
        args.image_json_path = pathlib.Path(args.image_json_path).absolute()
        if args.image_json_path.is_symlink():
            parser.error('Do not use symlink and hard link for --image_json_path key. It is an insecure way.')

    if hasattr(args, 'file') and args.file:
        args.file = pathlib.Path(args.file).absolute()
        if args.file.is_symlink():
            parser.error('Do not use symlink and hard link for --file key. It is an insecure way. ')
        if not args.file.exists():
            parser.error(f'Cannot find specified Dockerfile: {str(args.file)}.')

    if not hasattr(args, 'rhel_platform'):
        args.rhel_platform = 'docker'
    if args.rhel_platform != 'docker' and args.os != 'rhel8':
        parser.error('Dockerfile generation intended for non-Docker platforms '
                     'is supported only for RHEL-based images')

    if hasattr(args, 'product_version') and args.product_version:
        fail_if_product_version_not_supported(args.product_version, parser)
        product_version = re.search(r'^\d{4}\.\d$', args.product_version)
        if product_version:
            # save product version YYYY.U as YYYY.U.0
            args.product_version = f'{product_version.group()}.0'

    if args.mode in ('gen_dockerfile', 'build', 'build_test', 'all'):
        if args.package_url and not args.package_url.startswith(('http://', 'https://', 'ftp://')):
            if args.source == 'local' and not pathlib.Path(args.package_url).exists():
                parser.error('Provided local path of the package should be relative to <root_project> folder '
                             f'or should be an http/https/ftp access scheme: {args.package_url}')
            elif args.source == 'url' and args.distribution != 'base':
                parser.error('Provided URL is not supported, use http://, https:// or ftp:// access scheme')
            elif args.source == 'local' and pathlib.Path(args.package_url).is_symlink():
                parser.error('Do not use symlink and hard link to specify local package url. '
                             'It is an insecure way.')

        if not args.python:
            if args.os in ('ubuntu20', 'rhel8'):
                args.python = 'python38'
            else:
                args.python = 'python310'

        if args.python == 'python38' and 'win' in args.os:
            if not hasattr(args, 'pre_stage_msbuild') or not args.pre_stage_msbuild:
                parser.error('Option --pre_stage_msbuild is required for Windows images to build the latest version '
                             'of Python 3.8')

        if not args.distribution and args.package_url:
            if '_runtime_' in args.package_url:
                args.distribution = 'runtime'
            elif '_dev_' in args.package_url:
                args.distribution = 'dev'
            else:
                parser.error(f'Cannot get distribution type from the package URL provided. {args.package_url} '
                             'Please specify --distribution directly.')
        #  set installation method for the package
        args.install_type = 'copy'

        # workaround for https://bugs.python.org/issue16399 issue
        if not args.device and 'win' not in args.os:
            if args.distribution == 'base':
                args.device = ['cpu']
            elif args.os == 'rhel8':
                args.device = ['cpu', 'gpu']
            else:
                args.device = ['cpu', 'gpu']  # 2022.3 v/h not supported
        elif not args.device:
            args.device = ['cpu']

        if not args.package_url and not args.product_version:
            latest_public_version = max(INTEL_OPENVINO_VERSION.__iter__())
            args.product_version = '2022.2.0' if latest_public_version <= '2022.2.0' else latest_public_version
        args.build_id = ''

        if not args.package_url and args.distribution not in ('base',):
            if not args.distribution or not args.product_version:
                parser.error('Insufficient arguments. Provide --package_url '
                             'or --distribution (with optional --product_version) arguments')
            if args.mode != 'gen_dockerfile' or args.rhel_platform == 'autobuild':
                dev_version = re.search(r'^\d{4}\.\d\.\d\.dev\d{8}$', args.product_version)
                if dev_version:
                    args.product_version = dev_version.group()
                else:
                    lts_version = re.search(r'(\d{4}\.\d\.\d)', args.product_version)
                    if lts_version:
                        args.product_version = lts_version.group()  # save product version YYYY.U.V
                    else:
                        parser.error(f'Cannot find package url for {args.product_version} version')
                with contextlib.suppress(KeyError):
                    args.package_url = INTEL_OPENVINO_VERSION[args.product_version][args.os][args.distribution]
                if not args.package_url:
                    parser.error(f'Cannot find package url for {args.product_version} version '
                                 f'and {args.distribution} distribution. Please specify --package_url directly.')

        if args.package_url and not args.build_id:
            dev_version = re.search(r'p_(\d{4}\.\d\.\d\.dev\d{8})', args.package_url)
            if dev_version:
                # save product version and build version as YYYY.U.V.devYYYYMMDD
                args.product_version = dev_version.group(1)
                args.build_id = args.product_version
            else:
                build_id = re.search(r'_(\d{4}\.\d\.\d)\.(\d{3,4})', args.package_url)
                if build_id:
                    # save product version YYYY.U.V.BBB
                    args.build_id = '.'.join(build_id.groups())
                    # save product version YYYY.U.V
                    args.product_version = build_id.group(1)
                else:
                    args.build_id = args.product_version

        if not args.dockerfile_name:
            devices = ''.join([d[0] for d in args.device])
            layers = '_'.join(args.layers)
            openshift = 'openshift_' if args.rhel_platform == 'openshift' else ''
            version = args.product_version
            if layers:
                args.dockerfile_name = f'openvino_{openshift}{layers}_{version}.dockerfile'
            else:
                args.dockerfile_name = f'openvino_{devices}_{openshift}{args.distribution}_{version}.dockerfile'

        if not hasattr(args, 'wheels_version') or not args.wheels_version:
            args.wheels_version = (args.product_version if args.build_id == args.product_version
                                   else f'{args.product_version}.*')

    if not hasattr(args, 'tags') or not args.tags:
        layers = '_'.join(args.layers)
        tgl_postfix = ''

        if layers:
            args.tags = [f'{args.os}_{layers}:'
                         f'{args.build_id if args.build_id else args.product_version}{tgl_postfix}',
                         f'{args.os}_{layers}:latest']
            if hasattr(args, 'tag_postfix') and args.tag_postfix:
                args.tags.append(f'{args.os}_{layers}:{args.build_id if args.build_id else args.product_version}'
                                 f'{tgl_postfix}{args.tag_postfix}')
        elif args.distribution == 'base':
            args.tags = [f'{args.os}_{args.distribution}_cpu:'
                         f'{args.product_version}',
                         f'{args.os}_{args.distribution}_cpu:latest']
            if hasattr(args, 'tag_postfix') and args.tag_postfix:
                args.tags.append(f'{args.os}_{args.distribution}_cpu:'
                                 f'{args.product_version}{args.tag_postfix}')
        else:
            args.tags = [f'{args.os}_{args.distribution}:'
                         f'{args.build_id if args.build_id else args.product_version}{tgl_postfix}',
                         f'{args.os}_{args.distribution}:latest']
            if hasattr(args, 'tag_postfix') and args.tag_postfix:
                args.tags.append(f'{args.os}_{args.distribution}:'
                                 f'{args.build_id if args.build_id else args.product_version}'
                                 f'{tgl_postfix}{args.tag_postfix}')

    if args.mode not in ('test', 'deploy'):
        args.year = args.build_id[:4] if args.build_id else args.product_version[:4]

    if args.mode == 'test' and not args.product_version:
        match = re.search(r':(\d{4}\.\d\.\d)', str(args.tags))
        if not match and args.package_url:
            match = re.search(r'p_(\d{4}\.\d\.\d)', args.package_url)
        if match:
            # save product version YYYY.U.V
            args.product_version = match.group(1)
        elif args.distribution == 'custom':
            latest_public_version = list(INTEL_OPENVINO_VERSION.keys())[-1]
            args.product_version = '2022.2.0' if latest_public_version <= '2022.2.0' else latest_public_version
        else:
            parser.error('Cannot get product_version from the package URL and docker image. '
                         'Please specify --product_version directly.')

    if args.mode in ('test') and (not hasattr(args, 'wheels_version') or not args.wheels_version):
        latest_public_version = max(INTEL_OPENVINO_VERSION.__iter__())
        latest_public_version = '2022.2.0' if latest_public_version <= '2022.2.0' else latest_public_version
        args.wheels_version = args.product_version if hasattr(args, 'product_version') else latest_public_version

    if hasattr(args, 'product_version'):
        fail_if_product_version_not_supported(args.product_version, parser)

    if hasattr(args, 'distribution') and args.distribution == 'custom':
        if subprocess.call(['docker', 'run', '--rm', args.tags[0], 'ls', 'extras/opencv'],  # nosec
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT) != 0:
            args.distribution = 'custom-no-cv'
        else:
            args.distribution = 'custom-full'

    if hasattr(args, 'distribution'):
        if not args.package_url and args.mode == 'test' and args.distribution == 'custom-no-cv':
            if args.product_version in INTEL_OPENVINO_VERSION:
                args.package_url = INTEL_OPENVINO_VERSION[args.product_version][args.os]['dev']
            else:
                parser.error(f'Cannot find URL to package with test dependencies for {args.product_version} release. '
                             f'Please specify --package_url directly')
    return args
