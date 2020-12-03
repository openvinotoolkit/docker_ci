# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('is_image_os', 'is_distribution')
@pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
@pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
class TestPythonBindings:
    def test_opencv_bindings(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                root / 'tests' / 'resources' / 'python_bindings': {'bind': '/opt/intel/openvino/python_bindings'},
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'sh /opt/intel/openvino/python_bindings/create_py.sh && '
             'python3 /tmp/python_bindings/opencv_bindings.py"',
             ],
            self.test_opencv_bindings.__name__, **kwargs,
        )

    def test_openvino_bindings(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                root / 'tests' / 'resources' / 'python_bindings': {'bind': '/opt/intel/openvino/python_bindings'},
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'sh /opt/intel/openvino/python_bindings/create_py.sh && '
             'python3 /tmp/python_bindings/openvino_bindings.py"',
             ],
            self.test_openvino_bindings.__name__, **kwargs,
        )

    @pytest.mark.parametrize('min_product_version', ['2021.1'], indirect=True)
    def test_ngraph_bindings(self, tester, image, min_product_version):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                root / 'tests' / 'resources' / 'python_bindings': {'bind': '/opt/intel/openvino/python_bindings'},
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'sh /opt/intel/openvino/python_bindings/create_py.sh && '
             'python3 /tmp/python_bindings/ngraph_bindings.py"',
             ],
            self.test_ngraph_bindings.__name__, **kwargs,
        )
