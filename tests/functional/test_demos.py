# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


class TestDemosLinux:

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_security_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d CPU '
             '-sample-options -no_show',
             ], self.test_security_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_security_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d GPU '
             '-sample-options -no_show',
             ], self.test_security_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_security_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d MYRIAD '
             '-sample-options -no_show',
             ], self.test_security_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_security_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d HDDL '
             '-sample-options -no_show',
             ], self.test_security_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_squeezenet_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d CPU',
             ], self.test_squeezenet_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_squeezenet_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d GPU',
             ], self.test_squeezenet_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_squeezenet_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d MYRIAD',
             ], self.test_squeezenet_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_squeezenet_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['apt update',
             'apt install -y sudo',
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d HDDL',
             ], self.test_squeezenet_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_crossroad_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "source /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac "source /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name person-vehicle-bike-detection-crossroad-0078 --precisions FP16 '
             '-o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac "source /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/crossroad_camera_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/'
             'FP16/person-vehicle-bike-detection-crossroad-0078.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU -no_show"',
             ],
            self.test_crossroad_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_crossroad_cpp_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name person-vehicle-bike-detection-crossroad-0078 '
             '--precisions FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/crossroad_camera_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/FP16/'
             'person-vehicle-bike-detection-crossroad-0078.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU -no_show"',
             ],
            self.test_crossroad_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_crossroad_cpp_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name person-vehicle-bike-detection-crossroad-0078 '
             '--precisions FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/crossroad_camera_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/FP16/'
             'person-vehicle-bike-detection-crossroad-0078.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD -no_show"',
             ],
            self.test_crossroad_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_crossroad_cpp_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name person-vehicle-bike-detection-crossroad-0078 '
             '--precisions FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/crossroad_camera_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/FP16/'
             'person-vehicle-bike-detection-crossroad-0078.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL -no_show"',
             ],
            self.test_crossroad_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_text_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d_td CPU -no_show"',
             ],
            self.test_text_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_text_cpp_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d_td GPU -no_show"',
             ],
            self.test_text_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_text_cpp_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d_td MYRIAD -no_show"',
             ],
            self.test_text_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_text_cpp_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d_td HDDL -no_show"',
             ],
            self.test_text_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_detection_ssd_python_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU --no_show"',
             ],
            self.test_detection_ssd_python_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_detection_ssd_python_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU --no_show"',
             ],
            self.test_detection_ssd_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_detection_ssd_python_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD --no_show"',
             ],
            self.test_detection_ssd_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_detection_ssd_python_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL --no_show"',
             ],
            self.test_detection_ssd_python_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_segmentation_cpp_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/segmentation_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/semantic-segmentation-adas-0001/FP16/'
             'semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU -no_show"',
             ],
            self.test_segmentation_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_segmentation_cpp_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/segmentation_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/semantic-segmentation-adas-0001/FP16/'
             'semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU -no_show"',
             ],
            self.test_segmentation_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_segmentation_cpp_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/segmentation_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/semantic-segmentation-adas-0001/FP16/'
             'semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD -no_show"',
             ],
            self.test_segmentation_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_segmentation_cpp_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/segmentation_demo '
             '-m /root/omz_demos_build/intel64/Release/intel/semantic-segmentation-adas-0001/FP16/'
             'semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL -no_show"',
             ],
            self.test_segmentation_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.xfail(reason='38545 issue')
    def test_segmentation_python_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'segmentation_demo/segmentation_demo.py '
             '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU"',
             ],
            self.test_segmentation_python_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_segmentation_python_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'segmentation_demo/segmentation_demo.py '
             '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU"',
             ],
            self.test_segmentation_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_segmentation_python_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'segmentation_demo/segmentation_demo.py '
             '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD"',
             ],
            self.test_segmentation_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_segmentation_python_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'segmentation_demo/segmentation_demo.py '
             '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL"',
             ],
            self.test_segmentation_python_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_object_detection_centernet_python_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/converter.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_centernet/object_detection_demo_centernet.py '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU --no_show"',
             ],
            self.test_object_detection_centernet_python_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_object_detection_centernet_python_gpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/converter.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_centernet/object_detection_demo_centernet.py '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU --no_show"',
             ],
            self.test_object_detection_centernet_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_object_detection_centernet_python_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/converter.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_centernet/object_detection_demo_centernet.py '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD --no_show"',
             ],
            self.test_object_detection_centernet_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_object_detection_centernet_python_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/converter.py '
             '--name ctdet_coco_dlav0_384 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_centernet/object_detection_demo_centernet.py '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL --no_show"',
             ],
            self.test_object_detection_centernet_python_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_action_recognition_python_cpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "apt update && apt install -y --no-install-recommends curl"',
             '/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
             'https://github.com/intel-iot-devkit/sample-videos/blob/master/'
             'head-pose-face-detection-female.mp4?raw=true"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name action-recognition-0001-encoder,action-recognition-0001-decoder --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'action_recognition/action_recognition.py '
             '-m_en /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-encoder/FP16/'
             'action-recognition-0001-encoder.xml '
             '-m_de /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-decoder/FP16/'
             'action-recognition-0001-decoder.xml '
             '-i /root/action_recognition.mp4 -d CPU --no_show"',
             ],
            self.test_action_recognition_python_cpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    def test_action_recognition_python_gpu(self, is_distribution, is_image_os, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "apt update && apt install -y --no-install-recommends curl"',
             '/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
             'https://github.com/intel-iot-devkit/sample-videos/blob/master/'
             'head-pose-face-detection-female.mp4?raw=true"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name action-recognition-0001-encoder,action-recognition-0001-decoder --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'action_recognition/action_recognition.py '
             '-m_en /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-encoder/FP16/'
             'action-recognition-0001-encoder.xml '
             '-m_de /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-decoder/FP16/'
             'action-recognition-0001-decoder.xml '
             '-i /root/action_recognition.mp4 -d GPU --no_show"',
             ],
            self.test_action_recognition_python_gpu.__name__,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.vpu
    def test_action_recognition_python_vpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "apt update && apt install -y --no-install-recommends curl"',
             '/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
             'https://github.com/intel-iot-devkit/sample-videos/blob/master/'
             'head-pose-face-detection-female.mp4?raw=true"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name action-recognition-0001-encoder,action-recognition-0001-decoder --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'action_recognition/action_recognition.py '
             '-m_en /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-encoder/FP16/'
             'action-recognition-0001-encoder.xml '
             '-m_de /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-decoder/FP16/'
             'action-recognition-0001-decoder.xml '
             '-i /root/action_recognition.mp4 -d MYRIAD --no_show"',
             ],
            self.test_action_recognition_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20'], indirect=True)
    @pytest.mark.hddl
    def test_action_recognition_python_hddl(self, is_distribution, is_image_os, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "apt update && apt install -y --no-install-recommends curl"',
             '/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
             'https://github.com/intel-iot-devkit/sample-videos/blob/master/'
             'head-pose-face-detection-female.mp4?raw=true"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name action-recognition-0001-encoder,action-recognition-0001-decoder --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'action_recognition/action_recognition.py '
             '-m_en /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-encoder/FP16/'
             'action-recognition-0001-encoder.xml '
             '-m_de /opt/intel/openvino/intel/action-recognition-0001/action-recognition-0001-decoder/FP16/'
             'action-recognition-0001-decoder.xml '
             '-i /root/action_recognition.mp4 -d HDDL --no_show"',
             ],
            self.test_action_recognition_python_hddl.__name__, **kwargs,
        )


class TestDemosWindows:

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_security_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\ && '
             'demo_security_barrier_camera.bat -d CPU -sample-options -no_show'],
            self.test_security_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_squeezenet_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\ && '
             'demo_squeezenet_download_convert_run.bat -d CPU'],
            self.test_squeezenet_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_crossroad_cpp_cpu(self, is_distribution, is_image_os, tester, image):
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

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_text_cpp_cpu(self, is_distribution, is_image_os, tester, image):
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
             '-m_td C:\\\\Users\\\\ContainerAdministrator\\\\Documents\\\\Intel\\\\OpenVINO\\\\'
             'omz_demos_build\\\\intel64\\\\Release\\\\intel\\\\'
             'text-detection-0004\\\\FP16\\\\text-detection-0004.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d_td CPU -no_show',
             ],
            self.test_text_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    @pytest.mark.xfail(reason='38545 issue')
    def test_detection_ssd_python_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\demos\\\\'
             'python_demos\\\\object_detection_demo_ssd_async\\\\object_detection_demo_ssd_async.py '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\vehicle-detection-adas-0002\\\\FP16\\\\'
             'vehicle-detection-adas-0002.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU --no_show',
             ],
            self.test_detection_ssd_python_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_segmentation_cpp_cpu(self, is_distribution, is_image_os, tester, image):
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

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_segmentation_python_cpu(self, is_distribution, is_image_os, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\tools\\\\'
             'downloader\\\\downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16',
             'cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\demos\\\\'
             'python_demos\\\\segmentation_demo\\\\segmentation_demo.py '
             '-m C:\\\\intel\\\\openvino\\\\intel\\\\semantic-segmentation-adas-0001\\\\FP16\\\\'
             'semantic-segmentation-adas-0001.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU',
             ],
            self.test_segmentation_python_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['dev', 'proprietary'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['winserver2019'], indirect=True)
    def test_object_detection_centernet_python_cpu(self, is_distribution, is_image_os, tester, image):
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
             'python C:\\\\intel\\\\openvino\\\\deployment_tools\\\\open_model_zoo\\\\demos\\\\'
             'python_demos\\\\object_detection_demo_centernet\\\\object_detection_demo_centernet.py '
             '-m C:\\\\intel\\\\openvino\\\\public\\\\ctdet_coco_dlav0_384\\\\FP16\\\\ctdet_coco_dlav0_384.xml '
             '-i C:\\\\intel\\\\openvino\\\\deployment_tools\\\\demo\\\\car_1.bmp -d CPU --no_show',
             ],
            self.test_object_detection_centernet_python_cpu.__name__, **kwargs,
        )
