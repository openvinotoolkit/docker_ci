# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib
import re

import pytest


@pytest.mark.usefixtures('_is_not_distribution')
@pytest.mark.parametrize('_is_not_distribution', [('base')], indirect=True)
class TestPyPiChanges:
    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'centos8', 'rhel8')], indirect=True)
    def test_pypi_changes_linux(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        pypi_log_folder = root / 'logs' / image_folder / 'pypi_changes'
        pypi_deps_origin_file_name = re.search(r'(.*_\d{4}\.\d)', image.split('/')[-1].replace(':', '_'))
        if pypi_deps_origin_file_name:
            pypi_deps_origin_file_name = f'{pypi_deps_origin_file_name.group(1)}.json'
        if not pypi_log_folder.exists():
            pypi_log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'pypi_deps': {'bind': '/tmp/pypi_deps', 'mode': 'rw'},  # nosec
                pypi_log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec
            },
        }
        tester.test_docker_image(
            image,
            [f'python3 /tmp/pypi_deps/pypi_deps_manager.py '
             f'--check -i {image} -l /tmp/logs --image_json /tmp/pypi_deps/{pypi_deps_origin_file_name}'],
            self.test_pypi_changes_linux.__name__, **kwargs,
        )

    @pytest.mark.save_pypi_deps
    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'centos8', 'rhel8')], indirect=True)
    def test_save_pypi_deps_linux(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        pypi_log_folder = root / 'logs' / image_folder / 'pypi_changes'
        if not pypi_log_folder.exists():
            pypi_log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'pypi_deps': {'bind': '/tmp/pypi_deps', 'mode': 'rw'},  # nosec
                pypi_log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec
            },
        }
        tester.test_docker_image(
            image,
            [f'python3 /tmp/pypi_deps/pypi_deps_manager.py --save -i {image} -l /tmp/logs'],
            self.test_save_pypi_deps_linux.__name__, **kwargs,
        )
