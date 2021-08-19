# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('data_dev', 'proprietary')], indirect=True)
class TestSpeechDemoWindows:
    def test_speech_recognition_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\ && '
             'demo_speech_recognition.bat --no-show'],
            self.test_speech_recognition_cpu.__name__, **kwargs,
        )


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
class TestDemosWindows:
    def test_security_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\ && '
             'demo_security_barrier_camera.bat -d CPU -sample-options -no_show'],
            self.test_security_cpu.__name__, **kwargs,
        )

    def test_squeezenet_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\ && '
             'demo_squeezenet_download_convert_run.bat -d CPU'],
            self.test_squeezenet_cpu.__name__, **kwargs,
        )

    def test_crossroad_cpp_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator', 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\demos\\\\build_demos_msvc.bat',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name person-vehicle-bike-detection-crossroad-0078 --precisions FP16 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\crossroad_camera_demo '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'person-vehicle-bike-detection-crossroad-0078\\\\FP16\\\\person-vehicle-bike-detection-crossroad-0078.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU -no_show',
             ],
            self.test_crossroad_cpp_cpu.__name__, **kwargs,
        )

    def test_text_cpp_cpu(self, tester, image, product_version):
        kwargs = {'user': 'ContainerAdministrator', 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\demos\\\\build_demos_msvc.bat',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name text-detection-0004 --precision FP16 -o C:\\\\Users\\\\ContainerAdministrator\\\\'
             'Documents\\\\Intel\\\\OpenVINO\\\\omz_demos_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\text_detection_demo '
             f'{"-dt image" if "2020" in product_version else ""} '
             '-m_td C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'text-detection-0004\\\\FP16\\\\text-detection-0004.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d_td CPU -no_show',
             ],
            self.test_text_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    def test_detection_ssd_python_cpu(self, tester, image, omz_python_demo_path):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\vehicle-detection-adas-0002\\\\FP16\\\\'
             'vehicle-detection-adas-0002.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU --no_show',
             ],
            self.test_detection_ssd_python_cpu.__name__, **kwargs,
        )

    def test_segmentation_cpp_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator', 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\demos\\\\build_demos_msvc.bat',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16 -o C:\\\\Users\\\\'
             'ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\segmentation_demo '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\semantic-segmentation-adas-0001\\\\'
             'FP16\\\\semantic-segmentation-adas-0001.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU -no_show',
             ],
            self.test_segmentation_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['segmentation'], indirect=True)
    def test_segmentation_python_cpu(self, tester, image, omz_python_demo_path):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\semantic-segmentation-adas-0001\\\\FP16\\\\'
             'semantic-segmentation-adas-0001.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU',
             ],
            self.test_segmentation_python_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    def test_object_detection_centernet_python_cpu(self, tester, image, omz_python_demo_path):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name ctdet_coco_dlav0_384 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\converter.py '
             '--name ctdet_coco_dlav0_384 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\public\\\\ctdet_coco_dlav0_384\\\\FP16\\\\ctdet_coco_dlav0_384.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU --no_show',
             ],
            self.test_object_detection_centernet_python_cpu.__name__, **kwargs,
        )
