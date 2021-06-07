# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_not_distribution', '_is_not_image_os')
@pytest.mark.parametrize('_is_not_image_os', [('winserver2019')], indirect=True)
@pytest.mark.parametrize('_is_not_distribution', [('base', 'custom-no-omz',
                                                   'custom-no-cv', 'custom-full')], indirect=True)
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

    @pytest.mark.usefixtures('_min_product_version', '_max_product_version', '_is_image_os', '_is_distribution')
    @pytest.mark.parametrize('_min_product_version', ['2021.1'], indirect=True)
    @pytest.mark.parametrize('_max_product_version', ['2021.3'], indirect=True)
    @pytest.mark.parametrize('_is_image_os', ['ubuntu18'], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev', 'data_dev', 'proprietary')], indirect=True)
    def test_conflict_pypi_deps_venv_tf2(self, tester, image):
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
            ['/bin/bash -o pipefail -ac "cd /opt/intel/venv_tf2 && . ./bin/activate && '
             'python3 -m pip check 2>&1 | tee /tmp/logs/pip_check_tf2.log || '
             'python3 /tmp/pypi_deps/process_pip_conflicts.py -f /tmp/logs/pip_check_tf2.log '
             '-w /tmp/pypi_deps/pip_known_issues.txt"',
             ],
            self.test_conflict_pypi_deps_venv_tf2.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_min_product_version', '_max_product_version', '_is_image_os', '_is_distribution')
    @pytest.mark.parametrize('_min_product_version', ['2021.1'], indirect=True)
    @pytest.mark.parametrize('_max_product_version', ['2021.3'], indirect=True)
    @pytest.mark.parametrize('_is_image_os', ['ubuntu18'], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev', 'data_dev', 'proprietary')], indirect=True)
    def test_gpl_pypi_deps_venv_tf2(self, tester, image):
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
            ['/bin/bash -ac "cd /opt/intel/venv_tf2 && . ./bin/activate && '
             'python3 -m pip freeze 2>&1 | tee /tmp/logs/pypi_deps_tf2.log"',
             '/bin/bash -ac "cd /opt/intel/venv_tf2 && . ./bin/activate && python3 -m pip install pipdeptree && '
             'python3 -m pipdeptree -e PyGObject 2>&1 | tee /tmp/logs/pypi_deps_tree_tf2.log"',
             '/bin/bash -ac "cd /opt/intel/venv_tf2 && . ./bin/activate && python3 -m pip install pip-licenses && '
             'pip-licenses --output-file /tmp/logs/pypi_licenses_tf2.log && '
             'pip-licenses -f json --output-file /tmp/logs/pypi_licenses_tf2.json"',
             'python3 /tmp/pypi_deps/get_gpl_packages.py -f /tmp/logs/pypi_licenses_tf2.json '
             '-l /tmp/logs/pypi_licenses_gpl_tf2.json',
             ],
            self.test_gpl_pypi_deps_venv_tf2.__name__, **kwargs,
        )
