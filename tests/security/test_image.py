# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib
import subprocess  # nosec
import sys
import logging
import pytest

from setup import SNYK_API, SNYK_TOKEN
from utils.loader import SNYK_URL
from utils.utilities import download_file

logger = logging.getLogger(__name__)


class TestSDLImage:
    @pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Snyk Linux docker image '
                                                                     'can not scan windows images')
    @pytest.mark.skipif(SNYK_TOKEN == '',  # noqa: S105 # nosec
                        reason='Missing snyk token to do test. Specify it in setup.py file')
    def test_snyk_linux(self, image, dockerfile, snyk_image):
        dockerfile_args = []
        if dockerfile:
            dockerfile_args.extend(['--file=', dockerfile])
        cmd_line = ['docker', 'run', '--rm', '-e', f'SNYK_API={SNYK_API}',  # noqa
                    '-e', f'SNYK_TOKEN={SNYK_TOKEN}', '-e', 'MONITOR=true',
                    '-v', f'{str(pathlib.Path(__file__).parent.parent.parent)}:/project',
                    '-v', '/var/run/docker.sock:/var/run/docker.sock',
                    snyk_image, 'test', '--docker', image, *dockerfile_args]
        process = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        process_out = process.stdout.decode().replace(SNYK_TOKEN, '*' * 6)
        cmd_line[6] = 'SNYK_TOKEN=******'
        if process.returncode != 0:
            pytest.fail(f'SDL snyk issues: {cmd_line}\n{process_out}')
        else:
            logger.info(f'SDL snyk output: {cmd_line}\n{process_out}')

    @pytest.mark.skipif(not sys.platform.startswith('win32'), reason="Linux doesn't support windows executable files")
    @pytest.mark.skipif(SNYK_TOKEN == '',  # noqa: S105 # nosec
                        reason='Missing snyk token to do test. Specify it in setup.py file')
    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', ['ubuntu18', 'ubuntu20', 'ubuntu22'], indirect=True)
    def test_snyk_windows(self, image, dockerfile):
        location = pathlib.Path(__file__).parent
        snyk_file = location / 'snyk.exe'
        download_file(SNYK_URL['windows'], snyk_file)
        dockerfile_args = []
        if dockerfile:
            dockerfile_args.extend(['--file=', dockerfile])

        process_clear = subprocess.run([f'"{str(snyk_file)}"', 'config', 'clear'],
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        if process_clear.returncode != 0:
            pytest.fail('snyk clear config was failed')
        cmd_line = [f'set SNYK_API={SNYK_API}&&',
                    f'"{str(snyk_file)}"', 'auth', SNYK_TOKEN, '&&', f'"{str(snyk_file)}"', 'test',
                    '--docker', image, *dockerfile_args]
        process = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        process_out = process.stdout.decode().replace(SNYK_TOKEN, '*' * 6)
        cmd_line[3] = '******'
        if process.returncode != 0:
            pytest.fail(f'SDL snyk issues: {cmd_line}\n{process_out}')
        else:
            logger.info(f'SDL snyk output: {cmd_line}\n{process_out}')
