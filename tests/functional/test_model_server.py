#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib

import pytest


class TestModelServerLinux:

    @pytest.mark.parametrize('is_image_os', ('ubuntu18',), indirect=True)
    @pytest.mark.parametrize('is_image', ('model_server',), indirect=True)
    def test_model_server_unit(self, is_image_os, is_image, tester, image, mount_root):
        children = [item for item in (pathlib.Path(mount_root) / 'openvino_dev').iterdir()]
        dev_root = children[0]
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
            'volumes': {dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                'bind': '/opt/intel/openvino/inference_engine/samples/cpp'},
                        dev_root / 'deployment_tools' / 'demo': {'bind': '/opt/intel/openvino/deployment_tools/demo'},
                        dev_root / 'deployment_tools' / 'open_model_zoo': {
                            'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo'},
                        dev_root / 'deployment_tools' / 'model_optimizer': {
                            'bind': '/opt/intel/openvino/deployment_tools/model_optimizer'},
                        },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "source .venv/bin/activate && '
             'python -m pip install -r OpenVINO-model-server/requirements-dev.txt && '
             'pytest -s -v OpenVINO-model-server/tests/unit"',
             ],
            self.test_model_server_unit.__name__, **kwargs,
        )
