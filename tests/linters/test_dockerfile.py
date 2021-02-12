# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib
import subprocess  # nosec
import sys

import pytest
from tests.conftest import switch_container_engine


class TestDockerfile:
    @pytest.mark.usefixtures('_hadolint_pull')
    def test_hadolint(self, dockerfile):
        cmd_line = ['docker', 'run', '--rm', '-i', 'hadolint/hadolint:latest']
        process = subprocess.run(cmd_line, input=b''.join(pathlib.Path(dockerfile).open('rb').readlines()),
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        if process.returncode != 0:
            pytest.fail(f'Linter handolint issues: {process.stdout.decode()}')
        else:
            print(f'Linter handolint output: {process.stdout.decode()}')

    @pytest.fixture(scope='module')
    def _hadolint_pull(self, docker_api):
        image_name = 'hadolint/hadolint:latest'
        if sys.platform.startswith('win32'):
            switch_container_engine('-SwitchLinuxEngine')
        docker_api.client.images.pull(image_name)
        yield
        docker_api.client.images.remove(image_name, force=True)
        if sys.platform.startswith('win32'):
            switch_container_engine('-SwitchWindowsEngine')
