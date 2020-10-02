# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


class TestDlStreamerLinux:
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_distribution', ['data_dev'], indirect=True)
    def test_draw_face_attributes_cpp_cpu(self, is_image_os, is_distribution, tester, image):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/data_processing/dl_streamer/samples && '
             './download_models.sh && cd cpp/draw_face_attributes && mkdir build && '
             'cd build && cmake ../ && make && '
             'curl -O https://d30ikxcvcet9xo.cloudfront.net/data/test_data/videos/face-demographics-walking.mp4 && '
             './draw_face_attributes -i face-demographics-walking.mp4 -n"'],
            self.test_draw_face_attributes_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_distribution', ['data_dev'], indirect=True)
    @pytest.mark.gpu
    def test_draw_face_attributes_cpp_gpu(self, is_image_os, is_distribution, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/data_processing/dl_streamer/samples && '
             './download_models.sh && cd cpp/draw_face_attributes && mkdir build && '
             'cd build && cmake ../ && make && '
             'curl -O https://d30ikxcvcet9xo.cloudfront.net/data/test_data/videos/face-demographics-walking.mp4 && '
             './draw_face_attributes -i face-demographics-walking.mp4 -n -d GPU"'],
            self.test_draw_face_attributes_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_distribution', ['data_dev'], indirect=True)
    @pytest.mark.vpu
    @pytest.mark.xfail(reason='Failed to construct OpenVINOImageInference. Can not init Myriad device: NC_ERROR.')
    def test_draw_face_attributes_cpp_vpu(self, is_image_os, is_distribution, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/data_processing/dl_streamer/samples && '
             './download_models.sh && cd cpp/draw_face_attributes && mkdir build && '
             'cd build && cmake ../ && make && '
             'curl -O https://d30ikxcvcet9xo.cloudfront.net/data/test_data/videos/face-demographics-walking.mp4 && '
             './draw_face_attributes -i face-demographics-walking.mp4 -n -d MYRIAD -p FP16"'],
            self.test_draw_face_attributes_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_distribution', ['data_dev'], indirect=True)
    @pytest.mark.hddl
    def test_draw_face_attributes_cpp_hddl(self, is_image_os, is_distribution, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/data_processing/dl_streamer/samples && '
             './download_models.sh && cd cpp/draw_face_attributes && mkdir build && '
             'cd build && cmake ../ && make && '
             'curl -O https://d30ikxcvcet9xo.cloudfront.net/data/test_data/videos/face-demographics-walking.mp4 && '
             './draw_face_attributes -i face-demographics-walking.mp4 -n -d HDDL"'],
            self.test_draw_face_attributes_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_distribution', ['data_dev'], indirect=True)
    def test_gst_launch_audio_detect(self, is_image_os, is_distribution, tester, image):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh',
             'apt update', 'apt install wget',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/data_processing/dl_streamer/samples/gst_launch/audio_detect && '
             './download_audio_models.sh && ./audio_event_detection.sh"'],
            self.test_gst_launch_audio_detect.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_distribution', ['data_dev'], indirect=True)
    def test_gst_launch_metapublish(self, is_image_os, is_distribution, tester, image):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/data_processing/dl_streamer/samples && '
             './download_models.sh && cd gst_launch/metapublish && ./metapublish.sh"'],
            self.test_gst_launch_metapublish.__name__, **kwargs,
        )
