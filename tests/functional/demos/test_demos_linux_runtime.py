# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib

import pytest


class TestDemosLinuxRuntime:
    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_detection_ssd_python_cpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
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
            ['install_dependencies/install_openvino_dependencies.sh -y',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU --no_show"',
             ], self.test_detection_ssd_python_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    @pytest.mark.gpu
    def test_detection_ssd_python_gpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
            'volumes': {
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
            ['install_dependencies/install_openvino_dependencies.sh -y',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU --no_show"',
             ], self.test_detection_ssd_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    @pytest.mark.vpu
    def test_detection_ssd_python_vpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'device_cgroup_rules': ['c 189:* rmw'],
            'mem_limit': '3g',
            'volumes': {
                '/dev/bus/usb': {
                    'bind': '/dev/bus/usb',
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
            ['install_dependencies/install_openvino_dependencies.sh -y',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD --no_show"',
             ], self.test_detection_ssd_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    @pytest.mark.hddl
    def test_detection_ssd_python_hddl(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/ion:/dev/ion'],
            'mem_limit': '3g',
            'volumes': {
                '/var/tmp': {'bind': '/var/tmp'},
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
            ['install_dependencies/install_openvino_dependencies.sh -y',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'object_detection_demo_ssd_async/object_detection_demo_ssd_async.py '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL --no_show"',
             ], self.test_detection_ssd_python_hddl.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    def test_segmentation_python_cpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'mem_limit': '3g',
            'volumes': {
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
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name semantic-segmentation-adas-0001 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             'segmentation_demo/segmentation_demo.py '
             '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/semantic-segmentation-adas-0001.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU"',
             ],
            self.test_segmentation_python_cpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    @pytest.mark.gpu
    def test_segmentation_python_gpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/dri:/dev/dri'],
            'mem_limit': '3g',
            'volumes': {
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
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
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

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    @pytest.mark.vpu
    def test_segmentation_python_vpu(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'device_cgroup_rules': ['c 189:* rmw'],
            'mem_limit': '3g',
            'volumes': {
                '/dev/bus/usb': {
                    'bind': '/dev/bus/usb',
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
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
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

    @pytest.mark.parametrize('is_distribution', ['runtime'], indirect=True)
    @pytest.mark.parametrize('is_image_os', ['ubuntu18', 'ubuntu20', 'centos7'], indirect=True)
    @pytest.mark.parametrize('is_not_image', ['model_server'], indirect=True)
    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_segmentation_python_hddl(self, is_distribution, is_image_os, is_not_image, tester, image, mount_root):
        dev_root = (pathlib.Path(mount_root) / 'openvino_dev').iterdir().__next__()
        kwargs = {
            'devices': ['/dev/ion:/dev/ion'],
            'mem_limit': '3g',
            'volumes': {
                '/var/tmp': {'bind': '/var/tmp'},
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
             'python3 -m pip install --no-cache-dir -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
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
