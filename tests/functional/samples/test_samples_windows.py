# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest

from utils.exceptions import FailedTest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', ['winserver2019'], indirect=True)
@pytest.mark.parametrize('_is_distribution', ['dev', 'proprietary'], indirect=True)
class TestSamplesWindows:
    def test_hello_classification_cpp_cpu(self, tester, image):
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
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp CPU',
             ], self.test_hello_classification_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_min_product_version')
    @pytest.mark.parametrize('_min_product_version', ['2021.2'], indirect=True)
    def test_hello_classification_cpp_fail(self, tester, image, caplog):
        kwargs = {'user': 'ContainerAdministrator'}
        with pytest.raises(FailedTest):
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
                 'vehicle-attributes-recognition-barrier-0039\\\\FP16\\\\'
                 'vehicle-attributes-recognition-barrier-0039.xml '
                 'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car.png CPU',
                 ], self.test_hello_classification_cpp_fail.__name__, **kwargs,
            )
        if 'Sample supports topologies with 1 output only' not in caplog.text:
            pytest.fail('Sample supports topologies with 1 output only')

    def test_object_detection_cpp_cpu(self, tester, image):
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

    def test_classification_async_cpp_cpu(self, tester, image):
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
