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
from utils.exceptions import FailedTestError
from utils.tester import DockerImageTester
from utils.utilities import download_file, unzip_file

log = logging.getLogger('docker_ci')


def pytest_addoption(parser):
    parser.addoption('--registry', action='store', help='Setup a registry to pull the image from (optional)')
    parser.addoption('--dockerfile', action='store', help='Setup a dockerfile for check')
    parser.addoption('--image', action='store', help='Setup an image name for check')
    parser.addoption('--distribution', action='store', help='Setup an product distribution for check')
    parser.addoption('--image_os', action='store', help='Setup an image os for check')
    parser.addoption('--mount_root', action='store', help='Root folder for directories to mount to container')
    parser.addoption('--package_url', action='store', help='Path to product package')
    parser.addoption('--wheels_url', action='store', help='URL to HTML page with links or local path relative to '
                                                          'openvino folder to search for OpenVINO wheels')
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
    config.addinivalue_line(
        'markers', 'xfail_log: mark test as xfailed if caplog contains the specified pattern',
    )
    dist = config.getoption('--distribution')
    if dist in ('data_runtime', 'runtime', 'custom-no-cv'):
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
        if image_os in ('rhel8'):
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
                raise FailedTestError(err_msg)


@pytest.mark.hookwrapper()
def pytest_runtest_makereport(item, call):
    """Mark test as xfailed if caplog contains the specified pattern"""
    outcome = yield
    if call.when == 'call':
        for xfail_cond_marker in item.iter_markers('xfail_log'):
            report = outcome.get_result()
            if report.outcome == 'failed' and xfail_cond_marker.kwargs['pattern'] in report.caplog:
                report.outcome = 'skipped'
                report.wasxfail = f"reason: {xfail_cond_marker.kwargs['reason']}"


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
def tester(request):
    return DockerImageTester(request.config.getoption('--registry', default=''))


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
def wheels_url(request):
    return request.config.getoption('--wheels_url')


@pytest.fixture(scope='session')
def docker_api():
    return DockerAPI()


@pytest.fixture(scope='session')
def dev_root(request):
    openvino_dev_path = pathlib.Path(request.config.getoption('--mount_root')) / 'openvino_dev'
    dev_root_path = openvino_dev_path.iterdir().__next__()
    if dev_root_path.exists() and sum(f.stat().st_size if f.exists() else 0
                                      for f in openvino_dev_path.rglob('*')) < 10000000:
        pytest.skip(f'The test was skipped because the mount dependencies folder was not removed completely. '
                    f'Try to remove it manually via "sudo rm -r {openvino_dev_path}"')

    return dev_root_path


@pytest.fixture(scope='session')
def install_openvino_dependencies(request):
    image_os = request.config.getoption('--image_os')
    if 'ubuntu' in image_os:
        return '/bin/bash -ac "apt update && apt install -y build-essential curl cmake file"'
    elif 'rhel' in image_os:
        return '/bin/bash -ac "yum update -y && yum install -y make file"'
    return ''


@pytest.fixture(scope='session')
def install_openvino_dev_wheel(request):
    wheels_url = request.config.getoption('--wheels_url')
    image_os = request.config.getoption('--image_os')
    product_version = request.config.getoption('--product_version')

    def _install_openvino_dev_wheel(extras=''):
        python = 'python' if 'win' in image_os else 'python3'
        pip_install = f'{python} -m pip install --no-cache-dir'
        if wheels_url:
            return f'{pip_install} openvino_dev{extras}=={product_version} --trusted-host=* --find-links {wheels_url}'
        return f'{pip_install} --pre openvino_dev{extras}=={product_version}'
    return _install_openvino_dev_wheel


@pytest.fixture(scope='session')
def download_picture(request):
    image_os = request.config.getoption('--image_os')

    def _download_picture(picture, location=None):
        """Download a picture if it does not exist on Unix system only"""
        if not location:
            if 'win' in image_os:
                location = 'C:\\\\intel\\\\openvino\\\\samples\\\\'
            else:
                location = '/opt/intel/openvino/samples/'

        picture_on_share = f'https://storage.openvinotoolkit.org/data/test_data/images/{picture}'
        curl_cmd = f'curl -kL {picture_on_share} --output {location}{picture} --create-dirs '
        linux_cmd = (f'{curl_cmd} && ls -la {location} && '
                     f'file {location}{picture} &&'
                     f'file {location}{picture} | egrep \'PNG image data|bitmap|data\'')  # noqa: Q003
        if 'win' in image_os:
            return f'{curl_cmd}'
        else:
            return f'/bin/bash -ac "{linux_cmd}"'
    return _download_picture


@pytest.fixture(scope='session')
def bash(request):
    distribution = request.config.getoption('--distribution')

    def _bash(command):
        if distribution in ('base', 'custom-no-cv', 'custom-full'):
            return f'/bin/bash -ac ". /opt/intel/openvino/setupvars.sh && {command}"'
        else:
            return f'/bin/bash -c "{command}"'
    return _bash


@pytest.fixture()
def omz_python_demo_path(request):
    demo_name = request.param
    is_ssd = 'ssd' in request.node.name
    is_centernet = 'centernet' in request.node.name
    parameters = ''
    if demo_name == 'object_detection':
        if is_ssd:
            parameters = ' -at ssd'
        elif is_centernet:
            parameters = ' -at centernet'

    if 'win' in request.config.getoption('--image_os'):
        base_path = 'C:\\\\intel\\\\openvino\\\\demos'
        return f'{base_path}\\\\{demo_name}_demo\\\\python\\\\{demo_name}_demo.py{parameters}'
    else:
        base_path = '/opt/intel/openvino/demos'
        return f'{base_path}/{demo_name}_demo/python/{demo_name}_demo.py{parameters}'


@pytest.fixture(scope='session')
def omz_python_demos_requirements_file(request):
    base_path = '/opt/intel/openvino/extras/open_model_zoo/demos'
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


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason="Windows doesn't support linux images")
@pytest.fixture(scope='module')
def snyk_image(docker_api):
    image_name = 'snyk/snyk-cli:1.658.0-docker'
    docker_api.client.images.pull(image_name)
    yield image_name
    docker_api.client.images.remove(image_name, force=True)


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
    registry = request.config.getoption('--registry')
    image = f'{f"{registry}/" if registry else ""}{request.config.getoption("--image")}'
    if 'win' in request.config.getoption('--image_os'):
        command = ['docker', 'run', '--rm', image, 'cmd', '/c', 'dir /b/s python | findstr pyngraph']
    else:
        command = ['docker', 'run', '--rm', image, 'bash', '-c', 'find python | grep pyngraph']
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec
    if process.returncode != 0:
        pytest.skip('Test requires ngraph python bindings.')


@pytest.fixture(scope='session')
def _python_vpu_plugin_required(request):
    registry = request.config.getoption('--registry')
    image = f'{f"{registry}/" if registry else ""}{request.config.getoption("--image")}'
    if 'win' not in request.config.getoption('--image_os'):
        command = ['docker', 'run', '--rm', image, 'bash', '-c',
                   'find runtime/lib/intel64 | grep libmyriadPlugin.so']
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
