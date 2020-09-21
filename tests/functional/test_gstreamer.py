# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


class TestGstreamerLinux:
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_image', ['data_dev'], indirect=True)
    def test_gstreamer_python(self, is_image_os, is_image, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                root / 'tests' / 'resources' / 'gst_test': {'bind': '/opt/intel/openvino/gst_test'},
            },
        }
        tester.test_docker_image(
            image,
            ['/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh',
             'apt install -y python3-gst-1.0',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name face-detection-adas-0001 --precisions FP16 -o /tmp/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name age-gender-recognition-retail-0013 --precisions FP16 -o /tmp/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/gst_test && '
             'python3 detect_and_classify.py -i Fun_at_a_Fair_without_audio.mp4 '
             '-d /tmp/intel/face-detection-adas-0001/FP16/face-detection-adas-0001.xml '
             '-c /tmp/intel/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml"'
             ],
            self.test_gstreamer.__name__, **kwargs,
        )
