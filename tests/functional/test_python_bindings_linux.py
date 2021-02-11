# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest

root = pathlib.Path(os.path.realpath(__name__)).parent
kwargs = {
    'mem_limit': '3g',
    'volumes': {
        root / 'tests' / 'resources' / 'python_bindings': {'bind': '/opt/intel/openvino/python_bindings'},
    },
    'devices': ['/dev/dri:/dev/dri'],
}


@pytest.mark.usefixtures('_is_image_os', '_is_not_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'rhel8')], indirect=True)
class TestPythonBindingsLinux:
    @pytest.mark.parametrize('_is_not_distribution', [('base', 'custom-no-cv')], indirect=True)
    def test_opencv_bindings(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/python_bindings/opencv_bindings.py"',
             ],
            self.test_opencv_bindings.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_not_distribution', [('base')], indirect=True)
    def test_openvino_bindings(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/python_bindings/openvino_bindings.py"',
             ],
            self.test_openvino_bindings.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_min_product_version', '_python_ngraph_required')
    @pytest.mark.parametrize('_min_product_version', ['2021.1'], indirect=True)
    @pytest.mark.parametrize('_is_not_distribution', [('base')], indirect=True)
    def test_ngraph_bindings(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/python_bindings/ngraph_bindings.py"',
             ],
            self.test_ngraph_bindings.__name__, **kwargs,
        )
