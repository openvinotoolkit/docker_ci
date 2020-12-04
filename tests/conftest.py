# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import logging
import pathlib
import shutil
import subprocess  # nosec
import sys

import pytest
from utils.docker_api import DockerAPI
from utils.exceptions import FailedTest
from utils.tester import DockerImageTester
from utils.utilities import download_file, unzip_file

log = logging.getLogger('docker_ci')


def pytest_addoption(parser):
    parser.addoption('--dockerfile', action='store', help='Setup a dockerfile for check')
    parser.addoption('--image', action='store', help='Setup an image name for check')
    parser.addoption('--distribution', action='store', help='Setup an product distribution for check')
    parser.addoption('--image_os', action='store', help='Setup an image os for check')
    parser.addoption('--mount_root', action='store', help='Root folder for directories to mount to container')
    parser.addoption('--package_url', action='store', help='Path to product package')
    parser.addoption('--product_version', action='store', help='Setup a product_version for check')


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'hddl: run tests on HDDL device',
    )
    config.addinivalue_line(
        'markers', 'vpu: run tests on VPU device',
    )
    config.addinivalue_line(
        'markers', 'gpu: run tests on GPU device',
    )
    dist = config.getoption('--distribution')
    if dist == 'runtime':
        log.info('Setting up runtime image dependencies')
        mount_root = pathlib.Path(config.getoption('--mount_root'))
        package_url = config.getoption('--package_url')
        image_os = config.getoption('--image_os')
        if (mount_root / 'openvino_dev').exists():
            log.info('Directory for runtime testing dependency already exists, skipping dependency preparation')
            return

        if not package_url:
            return

        mount_root.mkdir(parents=True, exist_ok=True)
        dev_package_url = package_url.replace('_runtime_', '_dev_')
        # Temporarily, until there is no dev package for these distros
        if image_os in ('ubuntu20', 'centos7', 'centos8'):
            dev_package_url = dev_package_url.replace(image_os, 'ubuntu18')
        if package_url.startswith(('http://', 'https://', 'ftp://')):
            if 'win' in image_os:
                dldt_package = 'dldt.zip'
            else:
                dldt_package = 'dldt.tgz'
            log.info('Downloading dependent package...')
            download_file(
                dev_package_url,
                filename=mount_root / dldt_package,
                parents_=True,
                exist_ok_=True,
            )
            log.info('Extracting dependent package...')
            unzip_file(str(mount_root / dldt_package), str(mount_root / 'openvino_dev'))
            log.info('Dependent package downloaded and extracted')
        else:
            dev_package_archive = pathlib.Path(dev_package_url)
            if dev_package_archive.exists():
                unzip_file(str(dev_package_archive), str(mount_root / 'openvino_dev'))
                log.info('Dependent package extracted')
            else:
                err_msg = f"""Provided path of the dependent package should be an http/https/ftp access scheme
                                or a local file in the project location as dependent package: {package_url}"""
                log.error(err_msg)
                raise FailedTest(err_msg)


def pytest_sessionfinish(session, exitstatus):
    log.info(f'Tests failed={session.testsfailed} collected={session.testscollected}')
    temp_folder = pathlib.Path(__file__).parent / 'tmp'
    if not temp_folder.exists():
        return
    log.info('Removing mount dependencies')
    shutil.rmtree(temp_folder, ignore_errors=True)
    log.info('Cleanup completed')


@pytest.fixture(scope='session')
def tester():
    return DockerImageTester()


@pytest.fixture(scope='session')
def image(request):
    return request.config.getoption('--image')


@pytest.fixture(scope='session')
def mount_root(request):
    return request.config.getoption('--mount_root')


@pytest.fixture(scope='session')
def image_os(request):
    return request.config.getoption('--image_os')


@pytest.fixture(scope='session')
def dockerfile(request):
    return request.config.getoption('--dockerfile')


@pytest.fixture(scope='session')
def distribution(request):
    return request.config.getoption('--distribution')


@pytest.fixture(scope='session')
def package_url(request):
    return request.config.getoption('--package_url')


@pytest.fixture(scope='session')
def docker_api():
    return DockerAPI()


def switch_container_engine(engine):
    """Switch Windows docker Engine to -SwitchLinuxEngine or -SwitchWindowsEngine"""
    cmd_line = ['cmd', '/c', 'where', 'docker']
    process = subprocess.run(cmd_line,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)  # nosec
    if process.returncode != 0:
        pytest.fail(f'Can not find docker location on the host: {process.stdout.decode()}')
    docker_location = process.stdout.decode()
    docker_cli_location = pathlib.Path(docker_location).parent.parent.parent / 'DockerCli.exe'
    cmd_line = [str(docker_cli_location), engine]
    process = subprocess.run(cmd_line,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)  # nosec
    if process.returncode != 0:
        pytest.fail(f'Can not switch docker to: {engine}, error: {process.stdout.decode()}')


@pytest.fixture(scope='session')
def _is_distribution(request):
    settings = []
    if isinstance(request.param, str):
        settings.append(request.param)
    else:
        settings = request.param
    image_dist = request.config.getoption('--distribution')
    if not any(map(lambda x: x in image_dist, settings)):
        pytest.skip(f'Test requires the product distribution should be {request.param} but get '
                    f'{image_dist}')


@pytest.fixture(scope='session')
def _is_image_os(request):
    settings = []
    if isinstance(request.param, str):
        settings.append(request.param)
    else:
        settings = request.param
    image_os = request.config.getoption('--image_os')
    if not any(map(lambda x: x in image_os, settings)):
        pytest.skip(f'Test requires the image os should be {request.param} but get '
                    f'{image_os}')


@pytest.fixture(scope='session')
def _is_image(request):
    settings = []
    if isinstance(request.param, str):
        settings.append(request.param)
    else:
        settings = request.param
    image_name = request.config.getoption('--image')
    if not any(map(lambda x: x in image_name, settings)):
        pytest.skip(f'Test requires the image should be {request.param} but get '
                    f'{image_name}')


@pytest.fixture(scope='session')
def _is_not_image(request):
    settings = []
    if isinstance(request.param, str):
        settings.append(request.param)
    else:
        settings = request.param
    image_name = request.config.getoption('--image')
    if any(map(lambda x: x in image_name, settings)):
        pytest.skip(f'Test requires the image should not be {request.param} but get '
                    f'{image_name}')


@pytest.fixture(scope='session')
def _is_package_url_specified(request):
    if not request.config.getoption('--package_url'):
        pytest.skip('Test requires a url for a dev package.')


@pytest.fixture(scope='session')
def _min_product_version(request):
    image_version = request.config.getoption('--product_version')
    if image_version is not None and request.param > image_version:
        pytest.skip(f'Test requires the product_version should be {request.param} or newer '
                    f'but get {image_version}')


def pytest_generate_tests(metafunc):
    image_version = metafunc.config.getoption('--product_version')
    if image_version is None:
        return
    is_older = True if image_version <= '2021.1' else False
    is_ssd = True if 'ssd' in metafunc.definition.name else False
    is_centernet = True if 'centernet' in metafunc.definition.name else False
    if 'sample_name' in metafunc.fixturenames and is_older and is_ssd:
        metafunc.parametrize('sample_name', ['object_detection_demo_ssd_async/object_detection_demo_ssd_async.py'])
    elif 'sample_name' in metafunc.fixturenames and is_ssd and not is_older:
        metafunc.parametrize('sample_name', ['object_detection_demo/object_detection_demo.py -at ssd'])
    elif 'sample_name' in metafunc.fixturenames and is_centernet and is_older:
        metafunc.parametrize('sample_name', ['object_detection_demo_centernet/object_detection_demo_centernet.py'])
    elif 'sample_name' in metafunc.fixturenames and is_centernet and not is_older:
        metafunc.parametrize('sample_name', ['object_detection_demo/object_detection_demo.py -at centernet'])


def pytest_runtest_setup(item):
    for mark in item.iter_markers():
        if 'hddl' in mark.name and sys.platform.startswith('linux'):
            process = subprocess.run(['/bin/bash', '-c', 'pidof hddldaemon autoboot'],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     shell=False)  # nosec
            if process.returncode != 0:
                pytest.skip('Test requires running HDDL driver on the host machine')

        if 'vpu' in mark.name and sys.platform.startswith('linux'):
            # 03e7:2485 is a NCS2 device ID
            process = subprocess.run(['/bin/bash', '-c', 'lsusb | grep 03e7:2485'],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     shell=False)  # nosec
            if process.returncode != 0:
                pytest.skip('Test requires connected VPU device on the host machine')

        if 'gpu' in mark.name and sys.platform.startswith('linux'):
            process = subprocess.run(['/bin/bash', '-c', 'lspci | grep -E "VGA|3D"'],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     shell=False)  # nosec
            if process.returncode != 0:
                pytest.skip('Test requires Intel GPU device on the host machine')
