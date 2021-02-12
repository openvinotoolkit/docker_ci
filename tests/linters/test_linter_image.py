# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib
import subprocess  # nosec
import sys

import pytest

from utils.loader import DIVE_URL
from utils.utilities import download_file, unzip_file


class TestLinterImage:
    @pytest.mark.usefixtures('_dive_pull')
    @pytest.mark.skipif(not (sys.platform.startswith('linux') or sys.platform.startswith('darwin')),
                        reason='Windows has separate windows/linux docker images engine')
    def test_dive_linux(self, image):
        cmd_line = ['docker', 'run', '--rm', '-v', '/var/run/docker.sock:/var/run/docker.sock',
                    '-e', 'CI=true', 'wagoodman/dive:latest', image]
        process = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        if process.returncode != 0:
            pytest.fail(f'Linter dive issues: {process.stdout.decode()}')
        else:
            print(f'Linter dive output: {process.stdout.decode()}')

    @pytest.mark.skipif(not sys.platform.startswith('win32'), reason="Linux doesn't support windows executable files")
    def test_dive_windows(self, image):
        location = pathlib.Path(__file__).parent
        dive_zip_file = location / 'dive.zip'
        download_file(DIVE_URL['windows'], dive_zip_file)
        unzip_file(str(dive_zip_file), str(location))
        dive_file = location / 'dive.exe'
        cmd_line = [str(dive_file), '--ci', image]
        process = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        if process.returncode != 0:
            pytest.fail(f'Linter dive issues: {process.stdout.decode()}')
        else:
            print(f'Linter dive output: {process.stdout.decode()}')

    @pytest.mark.skipif(not (sys.platform.startswith('linux') or sys.platform.startswith('darwin')),
                        reason='Windows has separate windows/linux docker images engine')
    @pytest.fixture(scope='module')
    def _dive_pull(self, docker_api):
        image_name = 'wagoodman/dive:latest'
        docker_api.client.images.pull(image_name)
        yield
        docker_api.client.images.remove(image_name, force=True)
