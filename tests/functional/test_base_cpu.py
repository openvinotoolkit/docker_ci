# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
@pytest.mark.parametrize('is_distribution', ['base'], indirect=True)
def test_base_cpp(is_image_os, is_distribution, tester, image):
    root = pathlib.Path(os.path.realpath(__name__)).parent
    kwargs = {
        'mem_limit': '3g',
        'volumes': {
            root / 'tests' / 'resources' / 'base_cpu': {'bind': '/opt/intel/openvino/base_cpu'},
        },
    }
    tester.test_docker_image(
        image,
        ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
         '. /opt/intel/openvino/base_cpu/demo.sh"',
         ],
        test_base_cpp.__name__, **kwargs,
    )
