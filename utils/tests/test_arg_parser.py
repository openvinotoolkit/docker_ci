# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import argparse
import pathlib
from unittest import mock

import pytest

from utils.arg_parser import parse_args
from utils.loader import INTEL_OPENVINO_VERSION

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
    'ocl_release': '19.41.14441',
    'os': 'ubuntu18',
    'package_url': None,
    'product_version': None,
    'python': None,
    'source': 'url',
    'tags': None,
}


@pytest.mark.parametrize(('args', 'res'), [
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino.zip',
            'distribution': 'proprietary',
            'source': 'local',
            'product_version': '2020.1',
            'image_json_path': 'image_data.json',
        },
        {
            'device': ['cpu', 'gpu', 'vpu', 'hddl'],
            'dockerfile_name': 'openvino_cgvh_proprietary_2020.1.dockerfile',
            'python': 'python36',
            'tags': ['ubuntu18_proprietary:2020.1', 'ubuntu18_proprietary:latest'],
            'image_json_path': pathlib.Path('image_data.json').absolute(),
            'install_type': 'install',
        },
        id='set product_version, distribution and image_json_path manually',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
        },
        {
            'device': ['cpu', 'gpu', 'vpu', 'hddl'],
            'dockerfile_name': 'openvino_cgvh_dev_2020.1.dockerfile',
            'python': 'python36',
            'tags': ['ubuntu18_dev:2020.1.320', 'ubuntu18_dev:latest'],
            'distribution': 'dev',
            'install_type': 'copy',
            'product_version': '2020.1',
        },
        id='parse product_version and distribution from package_url',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'os': 'winserver2019',
        },
        {
            'device': ['cpu'],
            'dockerfile_name': 'openvino_c_dev_2020.1.dockerfile',
            'python': 'python37',
            'tags': ['winserver2019_dev:2020.1.320', 'winserver2019_dev:latest'],
            'distribution': 'dev',
            'product_version': '2020.1',
        },
        id='winserver2019',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'distribution': 'base',
            'file': 'openvino_c_base_2020.1.dockerfile',
            'source': 'local',
        },
        {
            'device': ['cpu'],
            'dockerfile_name': 'openvino_c_base_2020.1.dockerfile',
            'python': 'python36',
            'tags': ['ubuntu18_base_cpu:2020.1', 'ubuntu18_base_cpu:latest'],
            'distribution': 'base',
            'product_version': '2020.1',
        },
        id='ubuntu base',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'product_version': '2020.1',
        },
        {
            'device': ['cpu', 'gpu', 'vpu', 'hddl'],
            'python': 'python36',
            'dockerfile_name': 'openvino_cgvh_dev_2020.1.dockerfile',
            'tags': ['ubuntu18_dev:2020.1', 'ubuntu18_dev:latest'],
            'distribution': 'dev',
            'product_version': '2020.1',
        },
        id='build_id = product_version',
    ),
    pytest.param(
        {
            'mode': 'build',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'tags': ['my_tag:latest'],
            'device': ['cpu', 'hddl'],
        },
        {
            'device': ['cpu', 'hddl'],
            'python': 'python36',
            'dockerfile_name': 'openvino_ch_dev_2020.1.dockerfile',
            'tags': ['my_tag:latest'],
            'distribution': 'dev',
            'product_version': '2020.1',
        },
        id='set tags and device manually',
    ),
    pytest.param(
        {
            'mode': 'test',
            'distribution': 'dev',
            'tags': ['my_tag:latest'],
            'test_expression': 'cpu',
            'product_version': '2020.3',
        },
        {
        },
        id='(Test) Set product_version manually',
    ),
    pytest.param(
        {
            'mode': 'test',
            'distribution': 'dev',
            'tags': ['my_tag:latest'],
            'test_expression': 'cpu',
            'package_url': 'p_2020.3.117',
        },
        {
            'product_version': '2020.3',
        },
        id='(Test) Parse product_version from package_url',
    ),
    pytest.param(
        {
            'mode': 'test',
            'distribution': 'dev',
            'tags': ['my_tag:2020.3.117'],
            'test_expression': 'cpu',
        },
        {
            'product_version': '2020.3',
        },
        id='(Test) Parse product_version from tags',
    ),
    pytest.param(
        {
            'mode': 'all',
            'package_url': 'openvino_dev_p_2020.1.320.zip',
            'source': 'local',
            'registry': 'https://deploy',
        },
        {
            'device': ['cpu', 'gpu', 'vpu', 'hddl'],
            'python': 'python36',
            'tags': ['ubuntu18_dev:2020.1.320', 'ubuntu18_dev:latest'],
            'dockerfile_name': 'openvino_cgvh_dev_2020.1.dockerfile',
            'distribution': 'dev',
            'product_version': '2020.1',
        },
        id='Successful all',
    ),
    pytest.param(
        {
            'mode': 'deploy',
            'registry': 'https://deploy',
            'tags': ['deploy:latest'],
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
        },
        {
            'distribution': 'custom-no-cv',
            'product_version': list(INTEL_OPENVINO_VERSION.keys())[-1],
            'package_url': INTEL_OPENVINO_VERSION[list(INTEL_OPENVINO_VERSION.keys())[-1]]['ubuntu18']['dev'],
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
            'product_version': '2055.5',
        },
        'Cannot find package url for 2055.5 version and dev distribution. Please specify --package_url directly.',
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
            'distribution': 'dev',
        },
        'Insufficient arguments. Provide --package_url or --distribution and --product_version arguments',
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
            'package_url': 'https://openvino_p_2020.1.314_dev_pack.zip',
            'ocl_release': '1234',
        },
        'Provided Intel(R) Graphics Compute Runtime for OpenCL(TM) release is not acceptable',
        id='ocl_release error',
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
