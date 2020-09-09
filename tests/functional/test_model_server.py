# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


class TestModelServerLinux:

    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_image', ['model_server'], indirect=True)
    def test_model_server_unit(self, is_image_os, is_image, tester, image):
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "source .venv/bin/activate && '
             'python -m pip install -r OpenVINO-model-server/requirements-dev.txt && '
             'pytest -s -v OpenVINO-model-server/tests/unit"',
             ],
            self.test_model_server_unit.__name__, **kwargs,
        )
