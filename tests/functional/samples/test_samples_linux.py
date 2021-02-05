# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest

from utils.exceptions import FailedTest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary', 'custom-full')], indirect=True)
class TestSamplesLinux:
    def test_hello_classification_cpp_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png CPU"',
             ], self.test_hello_classification_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_hello_classification_cpp_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png GPU"',
             ], self.test_hello_classification_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    def test_hello_classification_cpp_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png MYRIAD"',
             ], self.test_hello_classification_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    def test_hello_classification_cpp_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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
             '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
             '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
             '/opt/intel/openvino/deployment_tools/demo/car.png HDDL"',
             ], self.test_hello_classification_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_min_product_version')
    @pytest.mark.parametrize('_min_product_version', ['2021.2'], indirect=True)
    def test_hello_classification_cpp_fail(self, tester, image, caplog, install_openvino_dependencies):
        with pytest.raises(FailedTest):
            tester.test_docker_image(
                image,
                [install_openvino_dependencies,
                 '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
                 'python3 -m pip install --no-cache-dir cmake setuptools && '
                 'cd /opt/intel/openvino/inference_engine/samples/cpp && '
                 '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
                 '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
                 'python3 -m pip install --no-cache-dir -r '
                 '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
                 'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
                 '--name vehicle-attributes-recognition-barrier-0039 --precisions FP32 '
                 '-o /root/inference_engine_cpp_samples_build/intel64/Release/"',
                 '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
                 '/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
                 '/root/inference_engine_cpp_samples_build/intel64/Release/intel/'
                 'vehicle-attributes-recognition-barrier-0039/FP32/'
                 'vehicle-attributes-recognition-barrier-0039.xml '
                 '/opt/intel/openvino/deployment_tools/demo/car.png CPU"',
                 ], self.test_hello_classification_cpp_fail.__name__,
            )
        if 'Sample supports topologies with 1 output only' not in caplog.text:
            pytest.fail('Sample supports topologies with 1 output only')

    def test_hello_reshape_cpp_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.gpu
    def test_hello_reshape_cpp_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.vpu
    def test_hello_reshape_cpp_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.hddl
    def test_hello_reshape_cpp_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    def test_object_detection_cpp_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.gpu
    def test_object_detection_cpp_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.vpu
    def test_object_detection_cpp_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.hddl
    def test_object_detection_cpp_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    def test_classification_async_cpp_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.gpu
    def test_classification_async_cpp_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.vpu
    def test_classification_async_cpp_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.hddl
    def test_classification_async_cpp_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    def test_benchmark_app_cpp_cpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/inference_engine/samples/cpp && '
             '/opt/intel/openvino/inference_engine/samples/cpp/build_samples.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name googlenet-v1 -o /root/inference_engine_cpp_samples_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'cd /opt/intel/openvino/deployment_tools/model_optimizer && '
             'python3 mo.py --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
             '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/googlenet-v1/'
             'googlenet-v1.caffemodel"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/inference_engine_cpp_samples_build/intel64/Release/benchmark_app '
             '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/googlenet-v1.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car.png -d CPU -api async --progress true"',
             ], self.test_benchmark_app_cpp_cpu.__name__, **kwargs,
        )
