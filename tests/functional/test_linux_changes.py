# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib
import re

import pytest


@pytest.mark.usefixtures('_is_not_distribution')
@pytest.mark.parametrize('_is_not_distribution', [('base')], indirect=True)
class TestLinuxChanges:
    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'centos8', 'rhel8')], indirect=True)
    def test_linux_deps_change(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        log_folder = root / 'logs' / image_folder / 'linux_deps'
        linux_deps_file_name = re.search(r'(.*_\d{4}\.\d)', image.split('/')[-1].replace(':', '_'))
        if linux_deps_file_name:
            linux_deps_file_name = f'{linux_deps_file_name.group(1)}.txt'
        if not log_folder.exists():
            log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'linux_deps': {'bind': '/tmp/linux_deps', 'mode': 'rw'},  # nosec
                log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh -p 2>&1 | '
             "sed 's/ /\\n/g' | tee /tmp/logs/install_openvino_dependencies_script_packages.log\"",
             f'/bin/bash -ac "python3 /tmp/linux_deps/linux_deps_compare.py -i {image} '
             f'-e /tmp/linux_deps/{linux_deps_file_name} '
             '-c /tmp/logs/install_openvino_dependencies_script_packages.log -l /tmp/logs"',
             ],
            self.test_linux_deps_change.__name__, **kwargs,
        )

    @pytest.mark.save_deps
    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'centos8', 'rhel8')], indirect=True)
    def test_save_linux_deps(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        log_folder = root / 'logs' / image_folder / 'linux_deps'
        linux_deps_file_name = re.search(r'(.*_\d{4}\.\d)', image.split('/')[-1].replace(':', '_'))
        if linux_deps_file_name:
            linux_deps_file_name = f'{linux_deps_file_name.group(1)}.txt'
        if not log_folder.exists():
            log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'linux_deps': {'bind': '/tmp/linux_deps', 'mode': 'rw'},  # nosec
                log_folder: {'bind': '/tmp/logs/linux_deps', 'mode': 'rw'},  # nosec
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh -p 2>&1 | '
             f"sed 's/ /\\n/g' | tee /tmp/linux_deps/{linux_deps_file_name}\"",
             ],
            self.test_save_linux_deps.__name__, **kwargs,
        )
