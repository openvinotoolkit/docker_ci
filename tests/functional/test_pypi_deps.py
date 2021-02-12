# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_not_distribution')
@pytest.mark.parametrize('_is_not_distribution', [('base')], indirect=True)
class TestPyPiDependencies:
    @pytest.mark.xfail(reason='47558 GPL Unidecode PyPi package as dependency for OMZ text_to_speech_demo')
    def test_gpl_pypi_deps(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        pypi_log_folder = root / 'logs' / image_folder / 'pypi_deps'
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
            ['/bin/bash -ac "python3 -m pip freeze 2>&1 | tee /tmp/logs/pypi_deps.log"',
             'python3 -m pip install pipdeptree',
             '/bin/bash -ac "python3 -m pipdeptree -e PyGObject 2>&1 | tee /tmp/logs/pypi_deps_tree.log"',
             'python3 -m pip install pip-licenses',
             'pip-licenses --output-file /tmp/logs/pypi_licenses.log',
             'pip-licenses -f json --output-file /tmp/logs/pypi_licenses.json',
             'python3 /tmp/pypi_deps/get_gpl_packages.py -f /tmp/logs/pypi_licenses.json '
             '-l /tmp/logs/pypi_licenses_gpl.json',
             ],
            self.test_gpl_pypi_deps.__name__, **kwargs,
        )

    def test_conflict_pypi_deps(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "python3 -m pip check"'],
            self.test_conflict_pypi_deps.__name__,
        )

    @pytest.mark.usefixtures('_is_image_os', '_is_distribution')
    @pytest.mark.parametrize('_is_image_os', ['ubuntu18'], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev', 'data_dev', 'proprietary')], indirect=True)
    def test_conflict_pypi_deps_venv_tf2(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "cd /opt/intel/venv_tf2 && . ./bin/activate && '
             'python3 -m pip check"',
             ],
            self.test_conflict_pypi_deps_venv_tf2.__name__,
        )

    @pytest.mark.usefixtures('_is_image_os', '_is_distribution')
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
                root / 'tests' / 'resources' / 'pypi_deps': {'bind': '/tmp/pypi_deps', 'mode': 'rw'},  # nosec
                pypi_log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec
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
