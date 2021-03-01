# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_image_os')
@pytest.mark.parametrize('_is_image_os', [('winserver2019')], indirect=True)
class TestPyPiDependenciesWindows:
    def test_gpl_pypi_deps(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        pypi_log_folder = root / 'logs' / image_folder / 'pypi_deps'
        if not pypi_log_folder.exists():
            pypi_log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'pypi_deps': {'bind': 'C:\\tmp\\pypi_deps', 'mode': 'rw'},  # nosec
                pypi_log_folder: {'bind': 'C:\\tmp\\logs', 'mode': 'rw'},  # nosec
            },
            'user': 'ContainerAdministrator',
        }
        tester.test_docker_image(
            image,
            ['cmd /S /C python -m pip freeze 2>&1 > C:\\\\tmp\\\\logs\\\\pypi_deps.log',
             'python -m pip install pipdeptree',
             'cmd /S /C python -m pipdeptree -e PyGObject 2>&1 > C:\\\\tmp\\\\logs\\\\pypi_deps_tree.log',
             'python -m pip install pip-licenses',
             'pip-licenses --output-file C:\\\\tmp\\\\logs\\\\pypi_licenses.log',
             'pip-licenses -f json --output-file C:\\\\tmp\\\\logs\\\\pypi_licenses.json',
             'python C:\\\\tmp\\\\pypi_deps\\\\get_gpl_packages.py -f C:\\\\tmp\\\\logs\\\\pypi_licenses.json '
             '-l C:\\\\tmp\\\\logs\\\\pypi_licenses_gpl.json -w C:\\\\tmp\\\\pypi_deps\\\\gpl_whitelist_rhel.txt',
             ],
            self.test_gpl_pypi_deps.__name__, **kwargs,
        )

    def test_conflict_pypi_deps(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        pypi_log_folder = root / 'logs' / image_folder / 'pypi_deps'
        if not pypi_log_folder.exists():
            pypi_log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'pypi_deps': {'bind': 'C:\\tmp\\pypi_deps', 'mode': 'rw'},  # nosec
                pypi_log_folder: {'bind': 'C:\\tmp\\logs', 'mode': 'rw'},  # nosec
            },
            'user': 'ContainerAdministrator',
        }
        tester.test_docker_image(
            image,
            ['cmd /S /C python -m pip check 2>&1 > C:\\\\tmp\\\\logs\\\\pip_check.log || '
             'python C:\\\\tmp\\\\pypi_deps\\\\process_pip_conflicts.py -f C:\\\\tmp\\\\logs\\\\pip_check.log '
             '-w C:\\\\tmp\\\\pypi_deps\\\\pip_known_issues.txt'],
            self.test_conflict_pypi_deps.__name__, **kwargs,
        )
