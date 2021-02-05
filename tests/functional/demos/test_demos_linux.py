# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('data_dev', 'proprietary')], indirect=True)
class TestDemosLinuxDataDev:
    def test_action_recognition_python_cpu(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
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

    @pytest.mark.gpu
    def test_action_recognition_python_gpu(self, tester, image):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
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
            self.test_action_recognition_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    def test_action_recognition_python_vpu(self, tester, image):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
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

    @pytest.mark.hddl
    def test_action_recognition_python_hddl(self, tester, image):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "curl -LJo /root/action_recognition.mp4 '
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


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary', 'custom-full')], indirect=True)
class TestDemosLinux:
    def test_security_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d CPU '
             '-sample-options -no_show',
             ], self.test_security_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_security_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d GPU '
             '-sample-options -no_show',
             ], self.test_security_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    def test_security_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d MYRIAD '
             '-sample-options -no_show',
             ], self.test_security_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    def test_security_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_security_barrier_camera.sh -d HDDL '
             '-sample-options -no_show',
             ], self.test_security_hddl.__name__, **kwargs,
        )

    def test_squeezenet_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d CPU',
             ], self.test_squeezenet_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_squeezenet_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d GPU',
             ], self.test_squeezenet_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    def test_squeezenet_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d MYRIAD',
             ], self.test_squeezenet_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    def test_squeezenet_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/deployment_tools/demo/demo_squeezenet_download_convert_run.sh -d HDDL',
             ], self.test_squeezenet_hddl.__name__, **kwargs,
        )

    def test_crossroad_cpp_cpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac "source /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.gpu
    def test_crossroad_cpp_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.vpu
    def test_crossroad_cpp_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.hddl
    def test_crossroad_cpp_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    def test_text_cpp_cpu(self, tester, image, product_version, install_openvino_dependencies):
        kwargs = {'mem_limit': '3g'}
        options = '-dt image' if '2021' not in product_version else ''  # legacy option, removed in 2021R
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             f'-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp {options} -d_td CPU -no_show"',
             ],
            self.test_text_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.gpu
    def test_text_cpp_gpu(self, tester, image, product_version, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        options = '-dt image' if '2021' not in product_version else ''
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             f'-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp {options} -d_td GPU -no_show"',
             ],
            self.test_text_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    def test_text_cpp_vpu(self, tester, image, product_version, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        options = '-dt image' if '2021' not in product_version else ''
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             f'-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp {options} -d_td MYRIAD -no_show"',
             ],
            self.test_text_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_text_cpp_hddl(self, tester, image, product_version, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        options = '-dt image' if '2021' not in product_version else ''
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/opt/intel/openvino/deployment_tools/open_model_zoo/demos/build_demos.sh"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name text-detection-0004 --precision FP16 -o /root/omz_demos_build/intel64/Release/"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             '/root/omz_demos_build/intel64/Release/text_detection_demo '
             '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
             f'-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp {options} -d_td HDDL -no_show"',
             ],
            self.test_text_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_detection_ssd_python_cpu(self, tester, image, sample_name):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU --no_show"',
             ],
            self.test_detection_ssd_python_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_detection_ssd_python_gpu(self, tester, image, sample_name):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU --no_show"',
             ],
            self.test_detection_ssd_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_detection_ssd_python_vpu(self, tester, image, sample_name):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD --no_show"',
             ],
            self.test_detection_ssd_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_detection_ssd_python_hddl(self, tester, image, sample_name):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/downloader.py '
             '--name vehicle-detection-adas-0002 --precision FP16"',
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
             'python3 /opt/intel/openvino/deployment_tools/open_model_zoo/demos/python_demos/'
             f'{sample_name} '
             '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL --no_show"',
             ],
            self.test_detection_ssd_python_hddl.__name__, **kwargs,
        )

    def test_segmentation_cpp_cpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.gpu
    def test_segmentation_cpp_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.vpu
    def test_segmentation_cpp_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_segmentation_cpp_hddl(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/bin/bash -ac ". /opt/intel/openvino/bin/setupvars.sh && '
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

    def test_segmentation_python_cpu(self, tester, image):
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

    @pytest.mark.gpu
    def test_segmentation_python_gpu(self, tester, image):
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

    @pytest.mark.vpu
    def test_segmentation_python_vpu(self, tester, image):
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

    @pytest.mark.hddl
    @pytest.mark.xfail(reason='38557 issue')
    def test_segmentation_python_hddl(self, tester, image):
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

    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_object_detection_centernet_python_cpu(self, tester, image, sample_name):
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
             f'{sample_name} '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d CPU --no_show"',
             ],
            self.test_object_detection_centernet_python_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_object_detection_centernet_python_gpu(self, tester, image, sample_name):
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
             f'{sample_name} '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d GPU --no_show"',
             ],
            self.test_object_detection_centernet_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_object_detection_centernet_python_vpu(self, tester, image, sample_name):
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
             f'{sample_name} '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d MYRIAD --no_show"',
             ],
            self.test_object_detection_centernet_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_object_detection_centernet_python_hddl(self, tester, image, sample_name):
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
             f'{sample_name} '
             '-m /opt/intel/openvino/public/ctdet_coco_dlav0_384/FP16/ctdet_coco_dlav0_384.xml '
             '-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -d HDDL --no_show"',
             ],
            self.test_object_detection_centernet_python_hddl.__name__, **kwargs,
        )
