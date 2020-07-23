#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib
import subprocess  # nosec
import sys

import pytest

from setup import SNYK_TOKEN
from utils.loader import SNYK_URL
from utils.utilities import download_file, set_windows_system_proxy


class TestSDLImage:

    @pytest.mark.skipif(not sys.platform.startswith('linux'), reason="Windows doesn't support linux images")
    @pytest.fixture(scope='module')
    def snyk_pull(self, docker_api):
        image_name = 'snyk/snyk-cli:docker'
        docker_api.client.images.pull(image_name)
        yield
        docker_api.client.images.remove(image_name)

    @pytest.mark.skipif(not sys.platform.startswith('linux'), reason="Windows doesn't support linux images")
    @pytest.mark.skipif(SNYK_TOKEN is None, reason='Missing snyk token to do test. Specify it in setup.py file')
    def test_snyk_linux(self, image, snyk_pull):
        cmd_line = ['docker', 'run', '--rm', '-it',
                    '-e', f'SNYK_TOKEN={SNYK_TOKEN}', '-e', 'MONITOR=true',
                    '-v', f'{str(pathlib.Path(__file__).parent.parent)}:/project',
                    '-v', '/var/run/docker.sock:/var/run/docker.sock',
                    'snyk/snyk-cli:docker', 'test', '--docker', image]
        process = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        if process.returncode != 0:
            pytest.fail(f'SDL snyk issues: {process.stdout.decode()}')
        else:
            print(f'SDL snyk output: {process.stdout.decode()}')

    @pytest.mark.skipif(not sys.platform.startswith('win32'), reason="Linux doesn't support windows executable files")
    @pytest.mark.skipif(SNYK_TOKEN is None, reason='Missing snyk token to do test. Specify it in setup.py file')
    def test_snyk_windows(self, get_proxy, image):
        location = pathlib.Path(__file__).parent
        snyk_file = location / 'snyk.exe'
        download_file(SNYK_URL['windows'], str(snyk_file), get_proxy)
        proxy = set_windows_system_proxy(get_proxy)
        cmd_line = [' && '.join(proxy), '&&', str(snyk_file), 'auth', SNYK_TOKEN, '&&', str(snyk_file), 'test',
                    '--docker', image]
        process = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        if process.returncode != 0:
            pytest.fail(f'SDL snyk issues: {process.stdout.decode()}')
        else:
            print(f'SDL snyk output: {process.stdout.decode()}')
