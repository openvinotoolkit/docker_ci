# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib

import pytest


class TestSamplesLinux:

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_hello_classification_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP32 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP32/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png CPU"',
             ], self.test_hello_classification_cpp_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_hello_classification_cpp_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP32 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP32/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png GPU"',
             ], self.test_hello_classification_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_hello_classification_cpp_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP32 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP32/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png MYRIAD"',
             ], self.test_hello_classification_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_hello_classification_cpp_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP32 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP32/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png HDDL"',
             ], self.test_hello_classification_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_hello_reshape_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp CPU 1"',
             ], self.test_hello_reshape_cpp_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_hello_reshape_cpp_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp GPU 1"',
             ], self.test_hello_reshape_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_hello_reshape_cpp_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp MYRIAD 1"',
             ], self.test_hello_reshape_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_hello_reshape_cpp_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp HDDL 1"',
             ], self.test_hello_reshape_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_object_detection_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU"',
             ], self.test_object_detection_cpp_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_object_detection_cpp_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU"',
             ], self.test_object_detection_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_object_detection_cpp_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD"',
             ], self.test_object_detection_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_object_detection_cpp_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL"',
             ], self.test_object_detection_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_classification_async_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name alexnet --precisions FP16 -o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/deployment_tools/model_optimizer && '
             'python3 mo.py --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
             '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
             'alexnet.caffemodel"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU"',
             ], self.test_classification_async_cpp_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_classification_async_cpp_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name alexnet --precisions FP16 -o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/deployment_tools/model_optimizer && '
             'python3 mo.py --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
             '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
             'alexnet.caffemodel"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU"',
             ], self.test_classification_async_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_classification_async_cpp_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name alexnet --precisions FP16 -o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/deployment_tools/model_optimizer && '
             'python3 mo.py --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
             '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
             'alexnet.caffemodel"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD"',
             ], self.test_classification_async_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_classification_async_cpp_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name alexnet --precisions FP16 -o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/deployment_tools/model_optimizer && '
             'python3 mo.py --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
             '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
             'alexnet.caffemodel"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL"',
             ], self.test_classification_async_cpp_hddl.__name__, **kwargs,
        )


class TestSamplesLinuxRuntime:

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_hello_classification_cpp_cpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
                dev_root / 'deployment_tools' / 'model_optimizer': {
                    'bind': '/opt/intel/openvino/deployment_tools/model_optimizer',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-attributes-recognition-barrier-0039 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/'
             'vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp CPU"',
             ], self.test_hello_classification_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_hello_classification_cpp_gpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-attributes-recognition-barrier-0039 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/'
             'vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp GPU"',
             ], self.test_hello_classification_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_hello_reshape_cpp_cpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
                dev_root / 'deployment_tools' / 'model_optimizer': {
                    'bind': '/opt/intel/openvino/deployment_tools/model_optimizer',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp CPU 1"',
             ], self.test_hello_reshape_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_hello_reshape_cpp_gpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
             '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '/opt/intel/openvino/deployment_tools/demo/car_1.bmp GPU 1"',
             ], self.test_hello_reshape_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_object_detection_cpp_cpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU"',
             ], self.test_object_detection_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_object_detection_cpp_gpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
             'vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU"',
             ], self.test_object_detection_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_classification_async_cpp_cpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
                dev_root / 'deployment_tools' / 'model_optimizer': {
                    'bind': '/opt/intel/openvino/deployment_tools/model_optimizer',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name alexnet --precisions FP16 -o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/model_optimizer/requirements.txt '
             '-r /opt/intel/openvino/deployment_tools/model_optimizer/requirements_caffe.txt && '
             'cd /opt/intel/openvino/deployment_tools/model_optimizer && '
             'python3 -B mo.py --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
             '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
             'alexnet.caffemodel"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU"',
             ], self.test_classification_async_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_classification_async_cpp_gpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
            'volumes': {
                dev_root / 'deployment_tools' / 'inference_engine' / 'samples' / 'cpp': {
                    'bind': '/opt/intel/openvino/inference_engine/samples/cpp',
                },
                dev_root / 'deployment_tools' / 'demo': {
                    'bind': '/opt/intel/openvino/deployment_tools/demo',
                },
                dev_root / 'deployment_tools' / 'open_model_zoo': {
                    'bind': '/opt/intel/openvino/deployment_tools/open_model_zoo',
                },
                dev_root / 'deployment_tools' / 'model_optimizer': {
                    'bind': '/opt/intel/openvino/deployment_tools/model_optimizer',
                },
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir '
             '-r /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 -B /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name alexnet --precisions FP16 -o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/deployment_tools/model_optimizer && '
             'python3 -m pip install --no-cache-dir -r requirements_caffe.txt && '
             'python3 -B mo.py --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
             '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
             'alexnet.caffemodel"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU"',
             ], self.test_classification_async_cpp_gpu.__name__, **kwargs,
        )


class TestSamplesWindows:
    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_hello_classification_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp && '
             'C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp\\\\build_samples_msvc.bat',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name vehicle-attributes-recognition-barrier-0039 --precisions FP16 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\hello_classification '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\intel\\\\'
             'vehicle-attributes-recognition-barrier-0039\\\\FP16\\\\vehicle-attributes-recognition-barrier-0039.xml '
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp CPU',
             ], self.test_hello_classification_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_hello_reshape_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp && '
             'C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp\\\\build_samples_msvc.bat',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\hello_reshape_ssd '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\intel\\\\'
             'vehicle-detection-adas-0002\\\\FP16\\\\vehicle-detection-adas-0002.xml '
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp CPU 1',
             ], self.test_hello_reshape_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_object_detection_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp && '
             'C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp\\\\build_samples_msvc.bat',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name vehicle-detection-adas-0002 --precisions FP16 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\object_detection_sample_ssd '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\intel\\\\'
             'vehicle-detection-adas-0002\\\\FP16\\\\vehicle-detection-adas-0002.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU',
             ], self.test_object_detection_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_classification_async_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp && '
             'C:\\\\intel\\\\openvino\\\\inference_engine\\\\samples\\\\cpp\\\\build_samples_msvc.bat',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name alexnet --precisions FP16 -o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\'
             'Intel\\\\OpenVINO\\\\inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\model_optimizer && '
             'python mo.py --output_dir C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\'
             'OpenVINO\\\\inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public '
             '--input_model C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public\\\\alexnet\\\\alexnet.caffemodel',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\classification_sample_async '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public\\\\alexnet.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU',
             ], self.test_classification_async_cpp_cpu.__name__, **kwargs,
        )


class TestSamplesWindowsRuntime:
    pass
