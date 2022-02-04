# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019', 'windows20h2')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
class TestDemosWindows:
    def test_security_cpu(self, omz_demos_win_cpu_tester, download_picture):
        omz_demos_win_cpu_tester.run_test(
            ['omz_downloader --name vehicle-license-plate-detection-barrier-0106 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'omz_downloader --name license-plate-recognition-barrier-0001 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\',
             'omz_downloader --name vehicle-attributes-recognition-barrier-0039 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\', download_picture('car_1.bmp'),
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
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp '
             '-d CPU -d_va CPU -d_lpr CPU -no_show'],
            self.test_security_cpu.__name__,
        )

    def test_crossroad_cpp_cpu(self, omz_demos_win_cpu_tester, download_picture):
        omz_demos_win_cpu_tester.run_test(
            ['omz_downloader --name person-vehicle-bike-detection-crossroad-0078 --precisions FP16 '
             '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\', download_picture('car_1.bmp'),
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\crossroad_camera_demo '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'person-vehicle-bike-detection-crossroad-0078\\\\FP16\\\\person-vehicle-bike-detection-crossroad-0078.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp -d CPU -no_show',
             ],
            self.test_crossroad_cpp_cpu.__name__,
        )

    def test_text_cpp_cpu(self, omz_demos_win_cpu_tester, download_picture):
        omz_demos_win_cpu_tester.run_test(
            ['omz_downloader --name text-detection-0004 --precision FP16 -o C:\\\\Users\\\\ContainerAdministrator\\\\'
             'Documents\\\\Intel\\\\OpenVINO\\\\omz_demos_build\\\\intel64\\\\Release\\\\',
             download_picture('car_1.bmp'),
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\text_detection_demo '
             '-m_td C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'text-detection-0004\\\\FP16\\\\text-detection-0004.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp -d_td CPU -no_show',
             ],
            self.test_text_cpp_cpu.__name__,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    def test_detection_ssd_python_cpu(self, omz_demos_win_cpu_tester, omz_python_demo_path, download_picture):
        omz_demos_win_cpu_tester.run_test(
            ['omz_downloader --name vehicle-detection-adas-0002 --precision FP16',
             download_picture('car_1.bmp'),
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\vehicle-detection-adas-0002\\\\FP16\\\\'
             'vehicle-detection-adas-0002.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp -d CPU --no_show',
             ],
            self.test_detection_ssd_python_cpu.__name__,
        )

    def test_segmentation_cpp_cpu(self, omz_demos_win_cpu_tester, download_picture):
        omz_demos_win_cpu_tester.run_test(
            ['omz_downloader --name semantic-segmentation-adas-0001 --precision FP16 -o C:\\\\Users\\\\'
             'ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\', download_picture('car_1.bmp'),
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\segmentation_demo '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\semantic-segmentation-adas-0001\\\\'
             'FP16\\\\semantic-segmentation-adas-0001.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp -d CPU -no_show',
             ],
            self.test_segmentation_cpp_cpu.__name__,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['segmentation'], indirect=True)
    def test_segmentation_python_cpu(self, omz_demos_win_cpu_tester, omz_python_demo_path, download_picture):
        omz_demos_win_cpu_tester.run_test(
            ['omz_downloader --name semantic-segmentation-adas-0001 --precision FP16',
             download_picture('car_1.bmp'),
             'cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             f'python {omz_python_demo_path} '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\semantic-segmentation-adas-0001\\\\FP16\\\\'
             'semantic-segmentation-adas-0001.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp -d CPU -at segmentation --no_show',
             ],
            self.test_segmentation_python_cpu.__name__,
        )
