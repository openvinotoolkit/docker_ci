# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import argparse
import pathlib
from unittest import mock

import pytest

from utils.arg_parser import parse_args

default_args = {
    'build_arg': [],
    'cmake': 'cmake314',
    'device': None,
    'distribution': None,
    'dockerfile_name': None,
    'file': None,
    'layers': [],
    'linter_check': [],
    # 'mode':'build',
    'msbuild': None,
    'pre_stage_msbuild': None,
    'rhel_platform': 'docker',
    'os': 'ubuntu18',
    'package_url': None,
    'product_version': None,
    'python': None,
    'source': 'url',
    'tags': None,
    'tag_postfix': '',
}


@pytest.mark.parametrize(('args', 'res'), [
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino.zip',
            'distribution': 'dev',
            'source': 'local',
            'product_version': '2022.1.0',
            'image_json_path': 'image_data.json',
        },
        {
            'device': ['cpu', 'gpu'],
            'dockerfile_name': 'openvino_cg_dev_2022.1.0.dockerfile',
            'python': 'python38',
            'tags': ['ubuntu18_dev:2022.1.0', 'ubuntu18_dev:latest'],
            'image_json_path': pathlib.Path('image_data.json').absolute(),
            'install_type': 'copy',
        },
        id='set product_version, distribution and image_json_path manually',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_genai_ubuntu22_2024.5.0.0_x86_64.tar.gz',
            'distribution': 'dev',
            'os': 'ubuntu22',
            'source': 'local',
        },
        {
            'device': ['cpu', 'gpu'],
            'dockerfile_name': 'openvino_cg_dev_2024.5.0.0.dockerfile',
            'python': 'python38',
            'tags': ['ubuntu22_dev:2024.5.0.0', 'ubuntu22_dev:latest'],
            'distribution': 'dev',
            'install_type': 'copy',
            'product_version': '2024.5.0.0',
        },
        id='parse product_version from package_url',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_genai_ubuntu22_2024.5.0.0_x86_64.tar.gz',
            'os': 'ubuntu22',
            'distribution': 'dev',
            'source': 'local',
            'tag_postfix': '_qqq',
        },
        {
            'device': ['cpu', 'gpu'],
            'dockerfile_name': 'openvino_cg_dev_2024.5.0.0.dockerfile',
            'python': 'python38',
            'tags': ['ubuntu22_dev:2024.5.0.0', 'ubuntu22_dev:latest', 'ubuntu22_dev:2024.5.0.0_qqq'],
            'distribution': 'dev',
            'install_type': 'copy',
            'product_version': '2024.5.0.0',
        },
        id='check tag postfix',
    ),
    # pytest.param(
    #     {
    #         'mode': 'build',
    #         'package_url': 'openvino_dev_p_2022.1.0.320.zip',
    #         'source': 'local',
    #         'os': 'winserver2019',
    #         'pre_stage_msbuild': 'msbuild2019_online',
    #     },
    #     {
    #         'device': ['cpu'],
    #         'dockerfile_name': 'openvino_c_dev_2022.1.0.dockerfile',
    #         'python': 'python38',
    #         'tags': ['winserver2019_dev:2022.1.0.320', 'winserver2019_dev:latest'],
    #         'distribution': 'dev',
    #         'product_version': '2022.1.0',
    #     },
    #     id='winserver2019',
    # ),
    # pytest.param(
    #     {
    #         'mode': 'build',
    #         'package_url': 'openvino_dev_p_2022.1.0.320.zip',
    #         'distribution': 'base',
    #         'file': 'openvino_c_base_2022.1.dockerfile',
    #         'source': 'local',
    #     },
    #     {
    #         'device': ['cpu'],
    #         'dockerfile_name': 'openvino_c_base_2022.1.0.dockerfile',
    #         'python': 'python38',
    #         'tags': ['ubuntu18_base_cpu:2022.1.0', 'ubuntu18_base_cpu:latest'],
    #         'distribution': 'base',
    #         'product_version': '2022.1.0',
    #     },
    #     id='ubuntu base',
    # ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2022.1.320.zip',
            'source': 'local',
            'product_version': '2022.1.0',
        },
        {
            'device': ['cpu', 'gpu'],
            'python': 'python38',
            'dockerfile_name': 'openvino_cg_dev_2022.1.0.dockerfile',
            'tags': ['ubuntu18_dev:2022.1.0', 'ubuntu18_dev:latest'],
            'distribution': 'dev',
            'product_version': '2022.1.0',
        },
        id='build_id = product_version',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2022.1.320.zip',
            'source': 'local',
            'product_version': '2022.1',
        },
        {
            'device': ['cpu', 'gpu'],
            'python': 'python38',
            'dockerfile_name': 'openvino_cg_dev_2022.1.0.dockerfile',
            'tags': ['ubuntu18_dev:2022.1.0', 'ubuntu18_dev:latest'],
            'distribution': 'dev',
            'product_version': '2022.1.0',
        },
        id='alias for product_version YYYY.U',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_genai_ubuntu22_2024.5.0.0.dev20240905_x86_64.tar.gz',
            'os': 'ubuntu22',
            'distribution': 'dev',
            'source': 'local',
        },
        {
            'device': ['cpu', 'gpu'],
            'python': 'python38',
            'dockerfile_name': 'openvino_cg_dev_2024.5.0.0.dev20240905.dockerfile',
            'tags': ['ubuntu22_dev:2024.5.0.0.dev20240905', 'ubuntu22_dev:latest'],
            'distribution': 'dev',
            'product_version': '2024.5.0.0.dev20240905',
            'build_id': '2024.5.0.0.dev20240905',
        },
        id='dev product version',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_genai_ubuntu22_2024.5.0.0.tar.gz',
            'source': 'local',
            'os': 'ubuntu22',
            'distribution': 'dev',
            'tags': ['my_tag:latest'],
            'device': ['cpu', 'gpu'],
        },
        {
            'device': ['cpu', 'gpu'],
            'python': 'python38',
            'dockerfile_name': 'openvino_ch_dev_2024.5.0.dockerfile',
            'tags': ['my_tag:latest'],
            'distribution': 'dev',
            'product_version': '2024.5.0.0',
        },
        id='set tags and device manually',
    ),
    pytest.param(
        {
            'mode': 'test',
            'distribution': 'dev',
            'tags': ['my_tag:latest'],
            'test_expression': 'cpu',
            'product_version': '2022.3.0',
        },
        {
            'wheels_version': '2022.3.0',
        },
        id='(Test) Set product_version manually',
    ),
    pytest.param(
        {
            'mode': 'test',
            'distribution': 'dev',
            'tags': ['my_tag:latest'],
            'test_expression': 'cpu',
            'package_url': 'p_2022.3.2.117',
        },
        {
            'product_version': '2022.3.2',
            'wheels_version': '2022.3.2',
        },
        id='(Test) Parse product_version from package_url',
    ),
    pytest.param(
        {
            'mode': 'test',
            'distribution': 'dev',
            'tags': ['my_tag:2022.3.1.117'],
            'test_expression': 'cpu',
        },
        {
            'product_version': '2022.3.1',
            'wheels_version': '2022.3.1',
        },
        id='(Test) Parse product_version from tags',
    ),
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_genai_ubuntu22_2024.5.0.0_x86_64.tar.gz',
            'source': 'local',
            'os': 'ubuntu22',
            'distribution': 'dev',
            'registry': 'https://deploy',
        },
        {
            'device': ['cpu', 'gpu'],
            'python': 'python38',
            'tags': ['ubuntu22_dev:2024.5.0.0', 'ubuntu22_dev:latest'],
            'dockerfile_name': 'openvino_cg_dev_2024.5.0.0.dockerfile',
            'distribution': 'dev',
            'product_version': '2024.5.0.0',
        },
        id='Successful all',
    ),
    pytest.param(
        {
            'mode': 'deploy',
            'registry': 'https://deploy',
            'tags': ['deploy:latest'],
            'product_version': '2022.1.1',
        },
        {
        },
        id='Successful deploy',
    ),
    pytest.param(
        {
            'mode': 'test',
            'tags': ['custom:no-cv'],
            'distribution': 'custom',
            'product_version': '2022.1.0',
            'package_url': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1.0/'
                           'l_openvino_toolkit_dev_ubuntu18_p_2022.1.0.582.tgz',
        },
        {
            'distribution': 'custom-no-cv',
            'product_version': '2022.1.0',
            'package_url': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1.0/'
                           'l_openvino_toolkit_dev_ubuntu18_p_2022.1.0.582.tgz',
        },
        id='Successful test custom image',
    ),

])
@mock.patch('utils.arg_parser.DockerCIArgumentParser.parse_args')
@mock.patch('pathlib.Path.exists')
def test_arg_parser_success(mock_exists, mock_parser, args, res):
    args = dict(list(default_args.items()) + list(args.items()))
    res = dict(list(args.items()) + list(res.items()))

    mock_exists.return_value = True
    mock_parser.return_value = argparse.Namespace(**args)

    out = vars(parse_args('', ''))
    for key in res:
        if out[key] != res[key] and key != 'file':
            pytest.fail(f'{key}: {out[key]} != {res[key]}')


@pytest.mark.parametrize(('args', 'parser_out'), [
    pytest.param(
        {
            'mode': 'gen_dockerfile',
            'distribution': 'base',
        },
        'Generating dockerfile for base distribution is not available',
        id='gen_dockerfile base error',
    ),
    pytest.param(
        {
            'mode': 'all',
            'distribution': 'base',
        },
        'The following argument is required: -f/--file',
        id='Build base image without --file',
    ),
    pytest.param(
        {
            'mode': 'build',
            'distribution': 'dev',
            'product_version': '2055.5.9',
        },
        'Cannot find package url for 2055.5.9 version and dev distribution. Please specify --package_url directly.',
        id='Incorrect openvino version',
    ),
    pytest.param(
        {
            'mode': 'deploy',
            'distribution': 'runtime',
        },
        'The following argument is required: -t/--tags',
        id='deploy --tags error',
    ),
    pytest.param(
        {
            'mode': 'build',
        },
        'Insufficient arguments. Provide --package_url or --distribution (with optional --product_version) arguments',
        id='Build without --package_url, --distribution, --product_version',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'https://openvino_p_2020.1.314_pack.zip',
        },
        'Cannot get distribution type from the package URL provided',
        id='distribution error',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2020.1.314.zip',
            'source': 'local',
        },
        'Provided local path of the package should be relative to',
        id='Local package path with --source local',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2020.1.314.zip',
        },
        'Provided URL is not supported, use http://, https:// or ftp:// access scheme',
        id='Local package path with --source url',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'http://openvino_dev_p_2020.1.314.zip',
            'sdl_check': ['kek'],
        },
        'Incorrect arguments for --sdl_check. Available tests: snyk, bench_security',
        id='sdl_check error',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'http://openvino_dev_p_2020.1.314.zip',
            'linter_check': ['kek'],
        },
        'Incorrect arguments for --linter_check. Available tests: hadolint, dive',
        id='linter_check error',
    ),
    pytest.param(
        {
            'mode': 'test',
            'distribution': 'dev',
            'test_expression': 'cpu',
        },
        'Options --tags and --distribution are mandatory. Image operation system is "ubuntu18" by default.',
        id='Test without --tags',
    ),
    pytest.param(
        {
            'mode': 'test',
            'test_expression': 'cpu',
            'tags': ['test:latest'],
        },
        'Options --tags and --distribution are mandatory. Image operation system is "ubuntu18" by default.',
        id='Test without --distribution',
    ),
    pytest.param(
        {
            'mode': 'deploy',
            'registry': 'https://deploy',
        },
        'The following argument is required: -t/--tags',
        id='Deploy without --tags',
    ),
    pytest.param(
        {
            'mode': 'deploy',
            'tags': ['deploy:latest'],
            'product_version': '2022.1',
        },
        'Option --registry is mandatory for this mode.',
        id='Deploy without --registry',
    ),
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'http://openvino_dev_p_2020.1.314.zip',
        },
        'Option --registry is mandatory for this mode.',
        id='All without --registry',
    ),
    pytest.param(
        {
            'mode': 'build',
            'tags': ['custom:no-cv'],
            'distribution': 'custom',
        },
        'For a custom distribution, only test and deploy modes are available.',
        id='Use custom image in not test or deploy mode',
    ),
    pytest.param(
        {
            'mode': 'build',
            'product_version': '2021.4',
            'distribution': 'dev',
        },
        'This version of the DockerHub CI framework does not support OpenVINO releases earlier than 2022.1.0.',
        id='Unsupported product_version',
    ),
])
@mock.patch('utils.arg_parser.DockerCIArgumentParser.parse_args')
def test_arg_parser_error(mock_parser, args, capsys, parser_out):
    args = dict(list(default_args.items()) + list(args.items()))

    mock_parser.return_value = argparse.Namespace(**args)

    with pytest.raises(SystemExit):
        parse_args('', '')

    out, err = capsys.readouterr()
    if parser_out not in err:
        pytest.fail(err)


@pytest.mark.parametrize(('args', 'exists', 'is_symlink', 'parser_out'), [  # noqa CFQ002
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'registry': 'https://deploy',
        },
        True,
        True,
        'Do not use symlink and hard link to specify local package url. It is an insecure way.',
        id='package_url is symlink',
    ),
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'registry': 'https://deploy',
        },
        False,
        False,
        'Provided local path of the package should be relative to <root_project>',
        id='package_url is not exists',
    ),
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'registry': 'https://deploy',
            'file': 'dockerfile',
        },
        True,
        True,
        'Do not use symlink and hard link for --file key. It is an insecure way',
        id='file is symlink',
    ),
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'registry': 'https://deploy',
            'file': 'dockerfile',
        },
        False,
        False,
        'Cannot find specified Dockerfile',
        id='file is not exists',
    ),
])
@mock.patch('utils.arg_parser.DockerCIArgumentParser.parse_args')
@mock.patch('pathlib.Path.exists')
@mock.patch('pathlib.Path.is_symlink')
def test_local_path(mock_is_symlink, mock_exists, mock_parser, args, exists, is_symlink, parser_out, capsys):
    args = dict(list(default_args.items()) + list(args.items()))
    mock_parser.return_value = argparse.Namespace(**args)

    mock_exists.return_value = exists
    mock_is_symlink.return_value = is_symlink

    with pytest.raises(SystemExit):
        parse_args('', '')

    out, err = capsys.readouterr()
    if parser_out not in err:
        pytest.fail(err)


@pytest.mark.parametrize(('args', 'is_symlink', 'parser_out'), [
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'registry': 'https://deploy',
            'image_json_path': 'qqq/qqq.json',
        },
        True,
        'Do not use symlink and hard link for --image_json_path key. It is an insecure way.',
        id='image_json_path is symlink',
    ),
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'registry': 'https://deploy',
            'image_json_path': 'qqq/qqq.json',
        },
        False,
        'Provided local path of the package should be relative to <root_project> folder or '
        'should be an http/https/ftp access scheme',
        id='image_json_path is not symlink but package_url local',
    ),
])
@mock.patch('utils.arg_parser.DockerCIArgumentParser.parse_args')
@mock.patch('pathlib.Path.is_symlink')
def test_symlink(mock_is_symlink, mock_parser, args, is_symlink, parser_out, capsys):
    args = dict(list(default_args.items()) + list(args.items()))
    mock_parser.return_value = argparse.Namespace(**args)

    mock_is_symlink.return_value = is_symlink

    with pytest.raises(SystemExit):
        parse_args('', '')

    out, err = capsys.readouterr()
    if parser_out not in err:
        pytest.fail(err)
