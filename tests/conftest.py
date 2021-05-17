# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import logging
import os
import pathlib
import shutil
import subprocess  # nosec
import sys

import pytest
from xdist.scheduler import LoadScopeScheduling
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
    config.addinivalue_line(
        'markers', 'save_deps: run test to save PyPi dependencies',
    )
    dist = config.getoption('--distribution')
    if dist in ('data_runtime', 'runtime', 'custom-no-omz', 'custom-no-cv'):
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
        if image_os in ('ubuntu20', 'centos7', 'centos8', 'rhel8'):
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
    if not temp_folder.exists() or os.getenv('PYTEST_XDIST_WORKER', 'master') != 'master':
        return
    log.info('Removing mount dependencies')
    shutil.rmtree(temp_folder, ignore_errors=True)
    log.info('Cleanup completed')


class OVDockerTestsScheduler(LoadScopeScheduling):
    """Custom parallel test scheduler
    """

    def _split_scope(self, nodeid):
        # run tests on HDDL device sequentially
        if 'hddl' in nodeid:
            return 'hddl'
        return super()._split_scope(nodeid)


def pytest_xdist_make_scheduler(log, config):
    return OVDockerTestsScheduler(config, log)


@pytest.fixture(scope='session')
def tester():
    return DockerImageTester()


@pytest.fixture(scope='session')
def image(request):
    return request.config.getoption('--image')


@pytest.fixture(scope='session')
def product_version(request):
    return request.config.getoption('--product_version')


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


@pytest.fixture(scope='session')
def dev_root(request):
    openvino_dev_path = pathlib.Path(request.config.getoption('--mount_root')) / 'openvino_dev'
    dev_root_path = openvino_dev_path.iterdir().__next__()
    if dev_root_path.exists() and sum(f.stat().st_size for f in openvino_dev_path.rglob('*')) < 10000000:
        pytest.skip(f'The test was skipped because the mount dependencies folder was not removed completely. '
                    f'Try to remove it manually via "sudo rm -r {openvino_dev_path}"')

    return dev_root_path


@pytest.fixture(scope='session')
def install_openvino_dependencies(request):
    image_os = request.config.getoption('--image_os')
    install_deps = '/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh'

    if '2020' in request.config.getoption('--product_version'):
        if 'ubuntu' in image_os:
            return f'/bin/bash -ac "apt update && apt install -y sudo && yes n | {install_deps}"'
        elif 'centos' in image_os:
            return f'/bin/bash -ac "yum update -y && yum install -y sudo && yes n | {install_deps}"'
    elif request.config.getoption('--product_version') < '2021.2':
        # installation of 3d party dependencies for data processing components isn't required since 2021.2
        return install_deps
    else:
        if 'ubuntu' in image_os:
            return '/bin/bash -ac "apt update && apt install -y build-essential sudo curl cmake"'
        elif any(x in image_os for x in ('centos', 'rhel')):
            return '/bin/bash -ac "yum update -y && yum install -y make"'
    return ''


@pytest.fixture()
def omz_python_demo_path(request):
    product_version = request.config.getoption('--product_version')
    demo_name = request.param
    is_ssd = 'ssd' in request.node.name
    is_centernet = 'centernet' in request.node.name
    parameters = ''
    if demo_name == 'object_detection':
        if is_ssd:
            parameters = ' -at ssd'
        elif is_centernet:
            parameters = ' -at centernet'
    if demo_name == 'segmentation' and product_version >= '2021.3':
        parameters = ' --no_show'

    if request.config.getoption('--image_os') == 'winserver2019':
        base_path = 'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\demos'
        if product_version <= '2021.1' and demo_name == 'object_detection':
            python_demos = f'{base_path}\\\\python_demos'
            if is_ssd:
                return f'{python_demos}\\\\object_detection_demo_ssd_async\\\\object_detection_demo_ssd_async.py'
            elif is_centernet:
                return f'{python_demos}\\\\object_detection_demo_centernet\\\\object_detection_demo_centernet.py'
            else:
                pytest.fail('This object_detection_demo parameter is not supported on the current image version')
        elif product_version <= '2021.2':
            demo_name += '_demo' if demo_name != 'action_recognition' else ''
            return f'{base_path}\\\\python_demos\\\\{demo_name}\\\\{demo_name}.py'
        else:
            return f'{base_path}\\\\{demo_name}_demo\\\\python\\\\{demo_name}_demo.py{parameters}'
    else:
        base_path = '/opt/intel/openvino/deployment_tools/open_model_zoo/demos'

        if product_version <= '2021.1' and demo_name == 'object_detection':
            if is_ssd:
                return f'{base_path}/python_demos/object_detection_demo_ssd_async/object_detection_demo_ssd_async.py'
            elif is_centernet:
                return f'{base_path}/python_demos/object_detection_demo_centernet/object_detection_demo_centernet.py'
            else:
                pytest.fail('This object_detection_demo parameter is not supported on the current image version')
        elif product_version <= '2021.2':
            demo_name += '_demo' if demo_name != 'action_recognition' else ''
            return f'{base_path}/python_demos/{demo_name}/{demo_name}.py{parameters}'
        else:
            return f'{base_path}/{demo_name}_demo/python/{demo_name}_demo.py{parameters}'


@pytest.fixture(scope='session')
def omz_python_demos_requirements_file(request):
    base_path = '/opt/intel/openvino/deployment_tools/open_model_zoo/demos'
    if request.config.getoption('--product_version') <= '2021.2':
        return f'{base_path}/python_demos/requirements.txt'
    else:
        return f'{base_path}/requirements.txt'


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
    settings = [request.param] if isinstance(request.param, str) else request.param
    image_dist = request.config.getoption('--distribution')
    if not any(map(lambda x: x in image_dist, settings)):
        pytest.skip(f'Test requires the product distribution should be {request.param} but get {image_dist}')


@pytest.fixture(scope='session')
def _is_not_distribution(request):
    settings = [request.param] if isinstance(request.param, str) else request.param
    image_dist = request.config.getoption('--distribution')
    if image_dist in settings:
        pytest.skip(f'Test requires the product distribution should not be {request.param} but get {image_dist}')


@pytest.fixture(scope='session')
def _is_not_image_os(request):
    settings = [request.param] if isinstance(request.param, str) else request.param
    image_os = request.config.getoption('--image_os')
    if image_os in settings:
        pytest.skip(f'Test requires the image os should not be {request.param} but get {image_os}')


@pytest.fixture(scope='session')
def _is_image_os(request):
    settings = [request.param] if isinstance(request.param, str) else request.param
    image_os = request.config.getoption('--image_os')
    if image_os not in settings:
        pytest.skip(f'Test requires the image os should be {request.param} but get {image_os}')


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


@pytest.fixture(scope='session')
def _max_product_version(request):
    image_version = request.config.getoption('--product_version')
    if image_version is not None and request.param < image_version:
        pytest.skip(f'Test requires the product_version should be {request.param} or older '
                    f'but get {image_version}')


@pytest.fixture(scope='session')
def _python_ngraph_required(request):
    image = request.config.getoption('--image')
    if request.config.getoption('--image_os') == 'winserver2019':
        command = ['docker', 'run', '--rm', image, 'cmd', '/c', 'dir /b/s python | findstr pyngraph']
    else:
        command = ['docker', 'run', '--rm', image, 'bash', '-c', 'find python | grep pyngraph']
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec
    if process.returncode != 0:
        pytest.skip('Test requires ngraph python bindings.')


@pytest.fixture(scope='session')
def _python_vpu_plugin_required(request):
    image = request.config.getoption('--image')
    if request.config.getoption('--image_os') != 'winserver2019':
        command = ['docker', 'run', '--rm', image, 'bash', '-c',
                   'find deployment_tools/inference_engine/lib/intel64 | grep libmyriadPlugin.so']
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec
        if process.returncode != 0:
            pytest.skip('Test requires VPU plugin.')


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

        is_save_key = 'save' in item.config.known_args_namespace.keyword
        is_deps_key = 'deps' in item.config.known_args_namespace.keyword
        if 'save_deps' in mark.name and not (is_save_key or is_deps_key):
            pytest.skip('Test should be executed directly -m save_deps -k <save_test_name>')
