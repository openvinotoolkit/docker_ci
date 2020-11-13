# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


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
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\hello_classification '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public\\\\alexnet.xml '
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car.png CPU',
             ], self.test_hello_classification_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    @pytest.mark.parametrize('is_not_product_version', ['2020.3'], indirect=True)
    @pytest.mark.xfail(reason='invalid model')
    def test_hello_classification_cpp_fail(self, is_distribution, is_image_os, tester, image, is_not_product_version):
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
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car.png CPU',
             ], self.test_hello_classification_cpp_fail.__name__, **kwargs,
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
