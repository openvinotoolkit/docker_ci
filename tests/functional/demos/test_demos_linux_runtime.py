# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution', '_is_package_url_specified')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'rhel8')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('data_runtime', 'custom-no-omz', 'custom-no-cv')], indirect=True)
class TestDemosLinuxDataRuntime:
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_detection_ssd_python_cpu(self, tester, image, distribution, dev_root, sample_name):
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
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU --no_show"',
             ], self.test_detection_ssd_python_cpu.__name__, **kwargs,
        )

    @pytest.mark.gpu
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_detection_ssd_python_gpu(self, tester, image, distribution, dev_root, sample_name):
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
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU --no_show"',
             ], self.test_detection_ssd_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.usefixtures('_python_ngraph_required', '_python_vpu_plugin_required')
    def test_detection_ssd_python_vpu(self, tester, image, distribution, dev_root, sample_name):
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
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD --no_show"',
             ], self.test_detection_ssd_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_detection_ssd_python_hddl(self, tester, image, distribution, dev_root, sample_name):
        kwargs = {
            'devices': ['/dev/ion:/dev/ion'],
            'mem_limit': '3g',
            'volumes': {
                '/var/tmp': {'bind': '/var/tmp'},  # nosec # noqa: S108
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
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/requirements.in && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL --no_show"',
             ], self.test_detection_ssd_python_hddl.__name__, **kwargs,
        )


@pytest.mark.usefixtures('_is_image_os', '_is_distribution', '_is_package_url_specified')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'rhel8')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('runtime', 'custom-no-omz', 'custom-no-cv')], indirect=True)
class TestDemosLinuxRuntime:
    def test_segmentation_python_cpu(self, tester, image, distribution, dev_root):
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
             'python3 -m pip install setuptools && '
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
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

    @pytest.mark.gpu
    def test_segmentation_python_gpu(self, tester, image, distribution, dev_root):
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
             'python3 -m pip install setuptools && '
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
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

    @pytest.mark.vpu
    @pytest.mark.usefixtures('_python_vpu_plugin_required')
    def test_segmentation_python_vpu(self, tester, image, distribution, dev_root):
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
             'python3 -m pip install setuptools && '
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
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

    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_segmentation_python_hddl(self, tester, image, distribution, dev_root):
        kwargs = {
            'devices': ['/dev/ion:/dev/ion'],
            'mem_limit': '3g',
            'volumes': {
                '/var/tmp': {'bind': '/var/tmp'},  # nosec # noqa: S108
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
             'python3 -m pip install setuptools && '
             f'python3 -m pip install --no-cache-dir {"opencv-python" if distribution == "custom-no-cv" else ""} -r '
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
