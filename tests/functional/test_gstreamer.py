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
                root / 'tests' / 'resources' / 'gst_sample': {'bind': '/opt/intel/openvino/gst_sample'},
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name face-detection-adas-0001 --precisions FP16 -o /tmp/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name age-gender-recognition-retail-0013 --precisions FP16 -o /tmp/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/gst_sample && '
             'curl -O https://d30ikxcvcet9xo.cloudfront.net/data/test_data/videos/face-demographics-walking.mp4 && '
             'python3 detect_and_classify.py -i face-demographics-walking.mp4 '
             '-d /tmp/intel/face-detection-adas-0001/FP16/face-detection-adas-0001.xml '
             '-c /tmp/intel/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml"',
             ],
            self.test_gstreamer_python.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_image', ['data_dev'], indirect=True)
    def test_gstreamer_cpp(self, is_image_os, is_image, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                root / 'tests' / 'resources' / 'gst_sample': {'bind': '/opt/intel/openvino/gst_sample'},
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name face-detection-adas-0001 -o /tmp/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name age-gender-recognition-retail-0013 -o /tmp/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cp -r /opt/intel/openvino/gst_sample/face_attributes /tmp && cd /tmp/face_attributes && mkdir build && '
             'cd build && cmake ../ && make && '
             'curl -O https://d30ikxcvcet9xo.cloudfront.net/data/test_data/videos/face-demographics-walking.mp4 && '
             './face_attributes -i face-demographics-walking.mp4 '
             '-m /tmp/intel/face-detection-adas-0001/FP32/face-detection-adas-0001.xml '
             '-c /tmp/intel/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml"',
             ],
            self.test_gstreamer_cpp.__name__, **kwargs,
        )
