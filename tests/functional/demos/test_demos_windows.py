# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019', 'windows20h2')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
class TestDemosWindows:
    def test_security_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\intel\\\\openvino\\\\extras\\\\open_model_zoo\\\\demos\\\\build_demos_msvc.bat',
             'omz_downloader --name vehicle-license-plate-detection-barrier-0106 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'omz_downloader --name license-plate-recognition-barrier-0001 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'omz_downloader --name vehicle-attributes-recognition-barrier-0039 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\security_barrier_camera_demo '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'vehicle-license-plate-detection-barrier-0106\\\\FP16\\\\vehicle-license-plate-detection-barrier-0106.xml '
             '-m_lpr C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'license-plate-recognition-barrier-0001\\\\FP16\\\\license-plate-recognition-barrier-0001.xml '
             '-m_va C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'vehicle-attributes-recognition-barrier-0039\\\\FP16\\\\vehicle-attributes-recognition-barrier-0039.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\car_1.bmp '
             '-d CPU -d_va CPU -d_lpr CPU -no_show'],
            self.test_security_cpu.__name__, **kwargs,
        )

    def test_squeezenet_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C cd C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\ && '
             'run_sample_squeezenet.bat -d CPU'],
            self.test_squeezenet_cpu.__name__, **kwargs,
        )

    def test_crossroad_cpp_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator', 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\intel\\\\openvino\\\\extras\\\\open_model_zoo\\\\demos\\\\build_demos_msvc.bat',
             'omz_downloader --name person-vehicle-bike-detection-crossroad-0078 --precisions FP16 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\crossroad_camera_demo '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'person-vehicle-bike-detection-crossroad-0078\\\\FP16\\\\person-vehicle-bike-detection-crossroad-0078.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\car_1.bmp -d CPU -no_show',
             ],
            self.test_crossroad_cpp_cpu.__name__, **kwargs,
        )

    def test_text_cpp_cpu(self, tester, image, product_version):
        kwargs = {'user': 'ContainerAdministrator', 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\intel\\\\openvino\\\\extras\\\\open_model_zoo\\\\demos\\\\build_demos_msvc.bat',
             'omz_downloader --name text-detection-0004 --precision FP16 -o C:\\\\Users\\\\ContainerAdministrator\\\\'
             'Documents\\\\Intel\\\\OpenVINO\\\\omz_demos_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\text_detection_demo '
             '-m_td C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'text-detection-0004\\\\FP16\\\\text-detection-0004.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\car_1.bmp -d_td CPU -no_show',
             ],
            self.test_text_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    def test_detection_ssd_python_cpu(self, tester, image, omz_python_demo_path):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['omz_downloader --name vehicle-detection-adas-0002 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\vehicle-detection-adas-0002\\\\FP16\\\\'
             'vehicle-detection-adas-0002.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\car_1.bmp -d CPU --no_show',
             ],
            self.test_detection_ssd_python_cpu.__name__, **kwargs,
        )

    def test_segmentation_cpp_cpu(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator', 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\intel\\\\openvino\\\\extras\\\\open_model_zoo\\\\demos\\\\build_demos_msvc.bat',
             'omz_downloader --name semantic-segmentation-adas-0001 --precision FP16 -o C:\\\\Users\\\\'
             'ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\segmentation_demo '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\semantic-segmentation-adas-0001\\\\'
             'FP16\\\\semantic-segmentation-adas-0001.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\car_1.bmp -d CPU -no_show',
             ],
            self.test_segmentation_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['segmentation'], indirect=True)
    def test_segmentation_python_cpu(self, tester, image, omz_python_demo_path):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['omz_downloader --name semantic-segmentation-adas-0001 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\semantic-segmentation-adas-0001\\\\FP16\\\\'
             'semantic-segmentation-adas-0001.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\car_1.bmp -d CPU -at segmentation --no_show',
             ],
            self.test_segmentation_python_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    def test_object_detection_centernet_python_cpu(self, tester, image, omz_python_demo_path):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['omz_downloader --name ctdet_coco_dlav0_384 --precision FP16',
             'omz_converter --name ctdet_coco_dlav0_384 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\public\\\\ctdet_coco_dlav0_384\\\\FP16\\\\ctdet_coco_dlav0_384.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\scripts\\\\car_1.bmp -d CPU --no_show',
             ],
            self.test_object_detection_centernet_python_cpu.__name__, **kwargs,
        )
