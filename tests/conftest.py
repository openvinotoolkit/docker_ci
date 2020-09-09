# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import logging
import pathlib
import shutil
import subprocess  # nosec
import sys
import tarfile
import zipfile

import pytest

from utils.docker_api import DockerAPI
from utils.exceptions import FailedTest
from utils.tester import DockerImageTester
from utils.utilities import download_file

log = logging.getLogger('project')


def pytest_addoption(parser):
    parser.addoption('--dockerfile', action='store', help='Setup a dockerfile for check')
    parser.addoption('--image', action='store', help='Setup an image name for check')
    parser.addoption('--distribution', action='store', help='Setup an product distribution for check')
    parser.addoption('--image_os', action='store', help='Setup an image os for check')
    parser.addoption('--mount_root', action='store', help='Root folder for directories to mount to container')
    parser.addoption('--package_url', action='store', help='Path to product package')


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'hddl: run tests on HDDL device',
    )
    dist = config.getoption('--distribution')
    if dist == 'runtime':
        log.info('Setting up runtime image dependencies')
        mount_root = pathlib.Path(config.getoption('--mount_root'))
        package_url = config.getoption('--package_url')
        image_os = config.getoption('--image_os')
        if not (mount_root / 'openvino_dev').exists():
            mount_root.mkdir(parents=True, exist_ok=True)
            if package_url.startswith(('http://', 'https://', 'ftp://')):
                log.info('Downloading dependent package...')
                if 'ubuntu' in image_os:
                    download_file(package_url.replace('_runtime_', '_dev_'),
                                  filename=mount_root / 'dldt.tgz',
                                  parents_=True, exist_ok_=True)
                    log.info('Extracting dependent package...')
                    with tarfile.open(str(mount_root / 'dldt.tgz'), 'r') as tar_file:
                        tar_file.extractall(str(mount_root / 'openvino_dev'))
                elif 'win' in image_os:
                    download_file(package_url.replace('_runtime_', '_dev_'),
                                  filename=mount_root / 'dldt.zip',
                                  parents_=True, exist_ok_=True)
                    log.info('Extracting dependent package...')
                    with zipfile.ZipFile(str(mount_root / 'dldt.zip'), 'r') as zip_file:
                        zip_file.extractall(str(mount_root / 'openvino_dev'))
                log.info('Dependent package downloaded and extracted')
            else:
                runtime_archive = pathlib.Path(package_url.replace('_runtime_', '_dev_'))
                if runtime_archive.exists():
                    if 'ubuntu' in image_os:
                        with tarfile.open(str(runtime_archive), 'r') as tar_file:
                            tar_file.extractall(str(mount_root / 'openvino_dev'))
                    elif 'win' in image_os:
                        with zipfile.ZipFile(str(runtime_archive), 'r') as zip_file:
                            zip_file.extractall(str(mount_root / 'openvino_dev'))
                    log.info('Dependent package extracted')
                else:
                    err_msg = f"""Provided path of the dependent package should be an http/https/ftp access scheme
                                    or a local file in the project location as dependent package: {package_url}"""
                    log.error(err_msg)
                    raise FailedTest(err_msg)
        else:
            log.info('Directory for runtime testing dependency already exists, skipping dependency preparation')


def pytest_unconfigure(config):
    temp_folder = pathlib.Path(__file__).parent / 'tmp'
    if not temp_folder.exists():
        return
    log.info('Removing mount dependencies')
    shutil.rmtree(temp_folder, ignore_errors=True)
    log.info('Cleanup completed')


def pytest_sessionfinish(session, exitstatus):
    log.info(f'Tests failed={session.testsfailed} collected={session.testscollected}')


@pytest.fixture(scope='session')
def dockerfile(request):
    return request.config.getoption('--dockerfile')


@pytest.fixture(scope='session')
def image(request):
    return request.config.getoption('--image')


@pytest.fixture(scope='session')
def distribution(request):
    return request.config.getoption('--distribution')


@pytest.fixture(scope='session')
def image_os(request):
    return request.config.getoption('--image_os')


@pytest.fixture(scope='session')
def mount_root(request):
    return request.config.getoption('--mount_root')


@pytest.fixture(scope='session')
def package_url(request):
    return request.config.getoption('--package_url')


@pytest.fixture(scope='session')
def docker_api():
    return DockerAPI()


@pytest.fixture(scope='session')
def tester():
    return DockerImageTester()


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
def is_distribution(request):
    settings = []
    if isinstance(request.param, str):
        settings.append(request.param)
    else:
        settings = request.param
    if not any(map(lambda x: x in request.config.getoption('--distribution'), settings)):
        pytest.skip(f'Test requires the product distribution should be {request.param} but get '
                    f'{request.config.getoption("--distribution")}')


@pytest.fixture(scope='session')
def is_image_os(request):
    settings = []
    if isinstance(request.param, str):
        settings.append(request.param)
    else:
        settings = request.param
    if not any(map(lambda x: x in request.config.getoption('--image_os'), settings)):
        pytest.skip(f'Test requires the image os should be {request.param} but get '
                    f'{request.config.getoption("--image_os")}')


@pytest.fixture(scope='session')
def is_image(request):
    settings = []
    if isinstance(request.param, str):
        settings.append(request.param)
    else:
        settings = request.param
    if not any(map(lambda x: x in request.config.getoption('--image'), settings)):
        pytest.skip(f'Test requires the image should be {request.param} but get '
                    f'{request.config.getoption("--image")}')


def pytest_runtest_setup(item):
    for mark in item.iter_markers():
        if 'hddl' in mark.name and sys.platform.startswith('linux'):
            process = subprocess.run(['/bin/bash', '-c', 'pidof hddldaemon autoboot'],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     shell=False)  # nosec
            if process.returncode != 0:
                pytest.skip('Test requires running HDDL driver on the host machine')
