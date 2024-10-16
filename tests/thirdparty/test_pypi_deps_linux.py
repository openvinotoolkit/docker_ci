# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_not_distribution', '_is_not_image_os')
@pytest.mark.parametrize('_is_not_image_os', [('winserver2019', 'windows20h2')], indirect=True)
@pytest.mark.parametrize('_is_not_distribution', [('base', 'custom-no-cv', 'custom-full')], indirect=True)
class TestPyPiDependenciesLinux:
    def test_gpl_pypi_deps(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        pypi_log_folder = root / 'logs' / image_folder / 'pypi_deps'
        if not pypi_log_folder.exists():
            pypi_log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'pypi_deps':
                    {'bind': '/tmp/pypi_deps', 'mode': 'rw'},  # nosec # noqa: S108
                pypi_log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec # noqa: S108
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "python3 -m pip freeze 2>&1 | tee /tmp/logs/pypi_deps.log"',
             'python3 -m pip install pipdeptree',
             '/bin/bash -ac "python3 -m pipdeptree -e PyGObject 2>&1 | tee /tmp/logs/pypi_deps_tree.log"',
             'python3 -m pip install pip-licenses',
             'pip-licenses --output-file /tmp/logs/pypi_licenses.log',
             'pip-licenses -f json --output-file /tmp/logs/pypi_licenses.json',
             'python3 /tmp/pypi_deps/get_gpl_packages.py -f /tmp/logs/pypi_licenses.json '
             '-l /tmp/logs/pypi_licenses_gpl.json -w /tmp/pypi_deps/gpl_whitelist_rhel.txt',
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
                root / 'tests' / 'resources' / 'pypi_deps':
                    {'bind': '/tmp/pypi_deps', 'mode': 'rw'},  # nosec # noqa: S108
                pypi_log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec # noqa: S108
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -o pipefail -ac "python3 -m pip check 2>&1 | tee /tmp/logs/pip_check.log || '
             'python3 /tmp/pypi_deps/process_pip_conflicts.py -f /tmp/logs/pip_check.log '
             '-w /tmp/pypi_deps/pip_known_issues.txt"'],
            self.test_conflict_pypi_deps.__name__, **kwargs,
        )
