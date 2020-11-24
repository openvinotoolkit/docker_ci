# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
def test_opencv_bindings(is_distribution, tester, image):
    py = """\
import cv2

print('OpenCV version:', cv2.getVersionString())
print('OpenVX:', cv2.haveOpenVX())
print('CPUs:', cv2.getNumberOfCPUs())
"""
    tester.test_docker_image(
        image,
        ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
         'mkdir -p /tmp/python_bindings && '
         f'printf \"{py}\" >> /tmp/python_bindings/opencv_bindings.py && '
         'python3 /tmp/python_bindings/opencv_bindings.py"',
         ],
        test_opencv_bindings.__name__,
    )


@pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
def test_openvino_bindings(is_distribution, tester, image):
    py = """\
import openvino.inference_engine as ie

print('OpenVINO version:', ie.get_version())
print('Available devices: ', ie.IECore().available_devices)
"""
    tester.test_docker_image(
        image,
        ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
         'mkdir -p /tmp/python_bindings && '
         f'printf \"{py}\" >> /tmp/python_bindings/openvino_bindings.py && '
         'python3 /tmp/python_bindings/openvino_bindings.py"',
         ],
        test_openvino_bindings.__name__,
    )


@pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
@pytest.mark.parametrize('min_product_version', ['2021.1'], indirect=True)
def test_ngraph_bindings(is_distribution, tester, image, min_product_version):
    py = """\
import ngraph
"""
    tester.test_docker_image(
        image,
        ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
         'mkdir -p /tmp/python_bindings && '
         f'printf \"{py}\" >> /tmp/python_bindings/ngraph_bindings.py && '
         'python3 /tmp/python_bindings/ngraph_bindings.py"',
         ],
        test_ngraph_bindings.__name__,
    )
