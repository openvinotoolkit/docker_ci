# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import subprocess  # nosec
import sys

import pytest


class TestSDLHost:
    @pytest.mark.usefixtures('_bench_security_pull')
    @pytest.mark.skipif(not sys.platform.startswith('linux'),
                        reason="Docker bench for security script doesn't support Windows host")
    def test_bench_security_linux(self):
        cmd_line = ['docker', 'run', '-it', '--net', 'host', '--pid', 'host', '--userns', 'host', '--cap-add',
                    'audit_control', '-e', 'DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST',
                    '-v', '/etc:/etc:ro', '-v', '/usr/bin/docker-containerd:/usr/bin/docker-containerd:ro',
                    '-v', '/usr/bin/docker-runc:/usr/bin/docker-runc:ro', '-v', '/usr/lib/systemd:/usr/lib/systemd:ro',
                    '-v', '/var/lib:/var/lib:ro', '-v', '/var/run/docker.sock:/var/run/docker.sock:ro',
                    '--label', 'docker_bench_security', 'docker/docker-bench-security']
        process = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)  # nosec
        if process.returncode != 0:
            pytest.fail(f'SDL Bench for security issues: {process.stdout.decode()}')
        else:
            print(f'SDL Bench for security output: {process.stdout.decode()}')

    @pytest.mark.skipif(not sys.platform.startswith('linux'),
                        reason="Docker bench for security script doesn't support Windows host")
    @pytest.fixture(scope='module')
    def _bench_security_pull(self, docker_api):
        image_name = 'docker/docker-bench-security:latest'
        docker_api.client.images.pull(image_name)
        yield
        docker_api.client.images.remove(image_name, force=True)
