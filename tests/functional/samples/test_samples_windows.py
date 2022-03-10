# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest

from utils.exceptions import FailedTestError


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019', 'windows20h2')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev')], indirect=True)
class TestSamplesWindows:
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_hello_classification_cpp_cpu(self, tester, image, download_picture):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\samples\\\\cpp && '
             'C:\\\\intel\\\\openvino\\\\samples\\\\cpp\\\\build_samples_msvc.bat',
             'omz_downloader --name alexnet --precisions FP16 -o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\'
             'Intel\\\\OpenVINO\\\\inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\',
             'mo --output_dir C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\'
             'OpenVINO\\\\inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public '
             '--input_model C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public\\\\alexnet\\\\alexnet.caffemodel',
             download_picture('car_1.bmp'),
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\hello_classification '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public\\\\alexnet.xml '
             'C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp CPU',
             ], self.test_hello_classification_cpp_cpu.__name__, **kwargs,
        )

    def test_hello_classification_cpp_fail(self, tester, image, caplog, download_picture):
        kwargs = {'user': 'ContainerAdministrator'}
        with pytest.raises(FailedTestError):
            tester.test_docker_image(
                image,
                ['cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
                 'cd C:\\\\intel\\\\openvino\\\\samples\\\\cpp && '
                 'C:\\\\intel\\\\openvino\\\\samples\\\\cpp\\\\build_samples_msvc.bat',
                 'omz_downloader --name vehicle-attributes-recognition-barrier-0039 --precisions FP16 '
                 '-o C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
                 'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\',
                 download_picture('car.png'),
                 'cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
                 'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
                 'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\hello_classification '
                 'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
                 'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\intel\\\\'
                 'vehicle-attributes-recognition-barrier-0039\\\\FP16\\\\'
                 'vehicle-attributes-recognition-barrier-0039.xml '
                 'C:\\\\intel\\\\openvino\\\\samples\\\\car.png CPU',
                 ], self.test_hello_classification_cpp_fail.__name__, **kwargs,
            )
        if 'Sample supports models with 1 output only' not in caplog.text:
            pytest.fail('Sample supports models with 1 output only')

    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_classification_async_cpp_cpu(self, tester, image, download_picture):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\samples\\\\cpp && '
             'C:\\\\intel\\\\openvino\\\\samples\\\\cpp\\\\build_samples_msvc.bat',
             'omz_downloader --name alexnet --precisions FP16 -o '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\'
             'Intel\\\\OpenVINO\\\\inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\',
             'mo --output_dir C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\'
             'OpenVINO\\\\inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public '
             '--input_model C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public\\\\alexnet\\\\alexnet.caffemodel',
             download_picture('car_1.bmp'),
             'cmd /S /C python -c "import cv2; img = cv2.imread(\'C:\\\\intel\\\\openvino\\\\samples\\\\car_1.bmp\', '
             'cv2.IMREAD_UNCHANGED); res = cv2.resize(img, (227,227)); '
             'cv2.imwrite(\'C:\\\\intel\\\\openvino\\\\samples\\\\car_1_227.bmp\', res)"',
             'cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\classification_sample_async '
             '-m C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'inference_engine_cpp_samples_build\\\\intel64\\\\Release\\\\public\\\\alexnet.xml '
             '-i C:\\\\intel\\\\openvino\\\\samples\\\\car_1_227.bmp -d CPU',
             ], self.test_classification_async_cpp_cpu.__name__, **kwargs,
        )
