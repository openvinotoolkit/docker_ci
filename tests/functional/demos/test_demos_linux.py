# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('data_dev', 'proprietary', 'custom-full')], indirect=True)
class TestDemosLinuxDataDev:
    @pytest.mark.parametrize('omz_python_demo_path', ['action_recognition'], indirect=True)
    def test_action_recognition_python_cpu(self, tester, image, omz_python_demo_path, bash):
        tester.test_docker_image(
            image,
            ['curl -LJo /root/action_recognition.mp4 https://github.com/intel-iot-devkit/sample-videos/blob/'
             'master/head-pose-face-detection-female.mp4?raw=true',
             bash('omz_downloader --name action-recognition-0001-encoder,action-recognition-0001-decoder '
                  '--precision FP16'),
             bash(f'python3 {omz_python_demo_path} -at en-de '
                  '-m_en /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-encoder/FP16/action-recognition-0001-encoder.xml '
                  '-m_de /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-decoder/FP16/action-recognition-0001-decoder.xml '
                  '-i /root/action_recognition.mp4 -d CPU --no_show'),
             ],
            self.test_action_recognition_python_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.parametrize('omz_python_demo_path', ['action_recognition'], indirect=True)
    def test_action_recognition_python_gpu(self, tester, image, omz_python_demo_path, bash):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            ['curl -LJo /root/action_recognition.mp4 https://github.com/intel-iot-devkit/sample-videos/blob/master/'
             'head-pose-face-detection-female.mp4?raw=true',
             bash('omz_downloader --name action-recognition-0001-encoder,action-recognition-0001-decoder '
                  '--precision FP16'),
             bash(f'python3 {omz_python_demo_path} -at en-de '
                  '-m_en /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-encoder/FP16/action-recognition-0001-encoder.xml '
                  '-m_de /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-decoder/FP16/action-recognition-0001-decoder.xml '
                  '-i /root/action_recognition.mp4 -d GPU --no_show'),
             ],
            self.test_action_recognition_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.parametrize('omz_python_demo_path', ['action_recognition'], indirect=True)
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    def test_action_recognition_python_vpu(self, tester, image, omz_python_demo_path, bash):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['curl -LJo /root/action_recognition.mp4 https://github.com/intel-iot-devkit/sample-videos/blob/master/'
             'head-pose-face-detection-female.mp4?raw=true',
             bash('omz_downloader --name action-recognition-0001-encoder,action-recognition-0001-decoder '
                  '--precision FP16'),
             bash(f'python3 {omz_python_demo_path} -at en-de '
                  '-m_en /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-encoder/FP16/action-recognition-0001-encoder.xml '
                  '-m_de /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-decoder/FP16/action-recognition-0001-decoder.xml '
                  '-i /root/action_recognition.mp4 -d MYRIAD --no_show'),
             ],
            self.test_action_recognition_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.parametrize('omz_python_demo_path', ['action_recognition'], indirect=True)
    def test_action_recognition_python_hddl(self, tester, image, omz_python_demo_path, bash):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            ['curl -LJo /root/action_recognition.mp4 https://github.com/intel-iot-devkit/sample-videos/blob/master/'
             'head-pose-face-detection-female.mp4?raw=true',
             bash('omz_downloader --name action-recognition-0001-encoder,action-recognition-0001-decoder '
                  '--precision FP16'),
             bash(f'umask 0000 && python3 {omz_python_demo_path} -at en-de '
                  '-m_en /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-encoder/FP16/action-recognition-0001-encoder.xml '
                  '-m_de /opt/intel/openvino/intel/action-recognition-0001/'
                  'action-recognition-0001-decoder/FP16/action-recognition-0001-decoder.xml '
                  '-i /root/action_recognition.mp4 -d HDDL --no_show && rm -f /dev/shm/hddl_*'),
             ],
            self.test_action_recognition_python_hddl.__name__, **kwargs,
        )


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary', 'custom-full')], indirect=True)
class TestDemosLinux:
    def test_crossroad_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=crossroad_camera_demo'),
             bash('omz_downloader --name person-vehicle-bike-detection-crossroad-0078 '
                  '--precisions FP16 '
                  '-o /root/omz_demos_build/intel64/Release/'), download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/crossroad_camera_demo '
                  '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/'
                  'FP16/person-vehicle-bike-detection-crossroad-0078.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d CPU -no_show'),
             ],
            self.test_crossroad_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.gpu
    def test_crossroad_cpp_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=crossroad_camera_demo'),
             bash('omz_downloader --name person-vehicle-bike-detection-crossroad-0078 '
                  '--precisions FP16 -o /root/omz_demos_build/intel64/Release/'), download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/crossroad_camera_demo '
                  '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/FP16/'
                  'person-vehicle-bike-detection-crossroad-0078.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d GPU -no_show'),
             ],
            self.test_crossroad_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_crossroad_cpp_vpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=crossroad_camera_demo'),
             bash('omz_downloader --name person-vehicle-bike-detection-crossroad-0078 '
                  '--precisions FP16 -o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/crossroad_camera_demo '
                  '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/FP16/'
                  'person-vehicle-bike-detection-crossroad-0078.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d MYRIAD -no_show'),
             ],
            self.test_crossroad_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_crossroad_cpp_hddl(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=crossroad_camera_demo'),
             bash('omz_downloader --name person-vehicle-bike-detection-crossroad-0078 '
                  '--precisions FP16 -o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('umask 0000 && /root/omz_demos_build/intel64/Release/crossroad_camera_demo '
                  '-m /root/omz_demos_build/intel64/Release/intel/person-vehicle-bike-detection-crossroad-0078/FP16/'
                  'person-vehicle-bike-detection-crossroad-0078.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d HDDL -no_show && rm -f /dev/shm/hddl_*'),
             ],
            self.test_crossroad_cpp_hddl.__name__, **kwargs,
        )

    def test_security_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=security_barrier_camera_demo'),
             bash('omz_downloader --name vehicle-license-plate-detection-barrier-0106 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name license-plate-recognition-barrier-0001 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name vehicle-attributes-recognition-barrier-0039 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/security_barrier_camera_demo '
                  '-i /opt/intel/openvino/samples/car_1.bmp '
                  '-m /root/omz_demos_build/intel64/Release/intel/vehicle-license-plate-detection-barrier-0106/'
                  'FP16/vehicle-license-plate-detection-barrier-0106.xml '
                  '-m_lpr /root/omz_demos_build/intel64/Release/intel/license-plate-recognition-barrier-0001/'
                  'FP16/license-plate-recognition-barrier-0001.xml '
                  '-m_va /root/omz_demos_build/intel64/Release/intel/vehicle-attributes-recognition-barrier-0039/'
                  'FP16/vehicle-attributes-recognition-barrier-0039.xml -no_show -d CPU -d_va CPU -d_lpr CPU'),
             ], self.test_security_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_security_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=security_barrier_camera_demo'),
             bash('omz_downloader --name vehicle-license-plate-detection-barrier-0106 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name license-plate-recognition-barrier-0001 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name vehicle-attributes-recognition-barrier-0039 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/security_barrier_camera_demo '
                  '-i /opt/intel/openvino/samples/car_1.bmp '
                  '-m /root/omz_demos_build/intel64/Release/intel/vehicle-license-plate-detection-barrier-0106/'
                  'FP16/vehicle-license-plate-detection-barrier-0106.xml '
                  '-m_lpr /root/omz_demos_build/intel64/Release/intel/license-plate-recognition-barrier-0001/'
                  'FP16/license-plate-recognition-barrier-0001.xml '
                  '-m_va /root/omz_demos_build/intel64/Release/intel/vehicle-attributes-recognition-barrier-0039/'
                  'FP16/vehicle-attributes-recognition-barrier-0039.xml -no_show -d GPU -d_va GPU -d_lpr GPU'),
             ], self.test_security_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_security_vpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=security_barrier_camera_demo'),
             bash('omz_downloader --name vehicle-license-plate-detection-barrier-0106 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name license-plate-recognition-barrier-0001 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name vehicle-attributes-recognition-barrier-0039 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/security_barrier_camera_demo '
                  '-i /opt/intel/openvino/samples/car_1.bmp '
                  '-m /root/omz_demos_build/intel64/Release/intel/vehicle-license-plate-detection-barrier-0106/'
                  'FP16/vehicle-license-plate-detection-barrier-0106.xml '
                  '-m_lpr /root/omz_demos_build/intel64/Release/intel/license-plate-recognition-barrier-0001/'
                  'FP16/license-plate-recognition-barrier-0001.xml '
                  '-m_va /root/omz_demos_build/intel64/Release/intel/vehicle-attributes-recognition-barrier-0039/'
                  'FP16/vehicle-attributes-recognition-barrier-0039.xml -no_show -d MYRIAD -d_va MYRIAD -d_lpr MYRIAD'),
             ], self.test_security_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_security_hddl(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=security_barrier_camera_demo'),
             bash('omz_downloader --name vehicle-license-plate-detection-barrier-0106 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name license-plate-recognition-barrier-0001 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             bash('omz_downloader --name vehicle-attributes-recognition-barrier-0039 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('umask 0000 && /root/omz_demos_build/intel64/Release/security_barrier_camera_demo '
                  '-i /opt/intel/openvino/samples/car_1.bmp '
                  '-m /root/omz_demos_build/intel64/Release/intel/vehicle-license-plate-detection-barrier-0106/'
                  'FP16/vehicle-license-plate-detection-barrier-0106.xml '
                  '-m_lpr /root/omz_demos_build/intel64/Release/intel/license-plate-recognition-barrier-0001/'
                  'FP16/license-plate-recognition-barrier-0001.xml '
                  '-m_va /root/omz_demos_build/intel64/Release/intel/vehicle-attributes-recognition-barrier-0039/'
                  'FP16/vehicle-attributes-recognition-barrier-0039.xml -no_show -d HDDL -d_va HDDL -d_lpr HDDL '
                  '-d HDDL -sample-options -no_show && rm -f /dev/shm/hddl_*"'),
             ], self.test_security_hddl.__name__, **kwargs,
        )

    def test_text_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=text_detection_demo'),
             bash('omz_downloader --name text-detection-0004 --precision FP16 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/text_detection_demo '
                  '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d_td CPU -no_show'),
             ],
            self.test_text_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.gpu
    def test_text_cpp_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=text_detection_demo'),
             bash('omz_downloader --name text-detection-0004 --precision FP16 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/text_detection_demo '
                  '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d_td GPU -no_show'),
             ],
            self.test_text_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_text_cpp_vpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=text_detection_demo'),
             bash('omz_downloader --name text-detection-0004 --precision FP16 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/text_detection_demo '
                  '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d_td MYRIAD -no_show'),
             ],
            self.test_text_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_text_cpp_hddl(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=text_detection_demo'),
             bash('omz_downloader --name text-detection-0004 --precision FP16 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('umask 0000 && /root/omz_demos_build/intel64/Release/text_detection_demo '
                  '-m_td /root/omz_demos_build/intel64/Release/intel/text-detection-0004/FP16/text-detection-0004.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d_td HDDL -no_show && '
                  'rm -f /dev/shm/hddl_*'),
             ],
            self.test_text_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_python_ngraph_required')
    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    def test_detection_ssd_python_cpu(self, tester, image, omz_python_demo_path, bash,
                                      install_openvino_dependencies, download_picture):
        tester.test_docker_image(
            image,
            [bash('omz_downloader --name vehicle-detection-adas-0002 --precision FP16'), install_openvino_dependencies,
             download_picture('car_1.bmp'),
             bash(f'python3 {omz_python_demo_path} '
                  '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d CPU --no_show -r'),
             ],
            self.test_detection_ssd_python_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.usefixtures('_python_ngraph_required')
    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    def test_detection_ssd_python_gpu(self, tester, image, omz_python_demo_path, bash,
                                      install_openvino_dependencies, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('omz_downloader --name vehicle-detection-adas-0002 --precision FP16'), install_openvino_dependencies,
             download_picture('car_1.bmp'),
             bash(f'python3 {omz_python_demo_path} '
                  '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d GPU --no_show -r'),
             ],
            self.test_detection_ssd_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.usefixtures('_python_ngraph_required', '_is_not_image_os')
    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_detection_ssd_python_vpu(self, tester, image, omz_python_demo_path, bash, download_picture,
                                      install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('omz_downloader --name vehicle-detection-adas-0002 --precision FP16'),
             download_picture('car_1.bmp'),
             bash(f'python3 {omz_python_demo_path} '
                  '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d MYRIAD --no_show -r'),
             ],
            self.test_detection_ssd_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_python_ngraph_required', '_is_not_image_os')
    @pytest.mark.parametrize('omz_python_demo_path', ['object_detection'], indirect=True)
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_detection_ssd_python_hddl(self, tester, image, omz_python_demo_path, bash, download_picture,
                                       install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('omz_downloader --name vehicle-detection-adas-0002 --precision FP16'),
             download_picture('car_1.bmp'),
             bash(f'umask 0000 && python3 {omz_python_demo_path} '
                  '-m /opt/intel/openvino/intel/vehicle-detection-adas-0002/FP16/vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d HDDL --no_show -r && '
                  'rm -f /dev/shm/hddl_*'),
             ],
            self.test_detection_ssd_python_hddl.__name__, **kwargs,
        )

    def test_segmentation_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'mem_limit': '4g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=segmentation_demo'),
             bash('omz_downloader --name semantic-segmentation-adas-0001 --precision FP16 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/segmentation_demo '
                  '-m /root/omz_demos_build/intel64/Release/intel/semantic-segmentation-adas-0001/FP16/'
                  'semantic-segmentation-adas-0001.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d CPU -no_show'),
             ],
            self.test_segmentation_cpp_cpu.__name__, **kwargs,
        )

    @pytest.mark.gpu
    def test_segmentation_cpp_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '4g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('/opt/intel/openvino/demos/build_demos.sh --target=segmentation_demo'),
             bash('omz_downloader --name semantic-segmentation-adas-0001 --precision FP16 '
                  '-o /root/omz_demos_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/omz_demos_build/intel64/Release/segmentation_demo '
                  '-m /root/omz_demos_build/intel64/Release/intel/semantic-segmentation-adas-0001/FP16/'
                  'semantic-segmentation-adas-0001.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d GPU -no_show'),
             ],
            self.test_segmentation_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.parametrize('omz_python_demo_path', ['segmentation'], indirect=True)
    def test_segmentation_python_cpu(self, tester, image, omz_python_demo_path, bash,
                                     install_openvino_dependencies, download_picture):
        tester.test_docker_image(
            image,
            [bash('omz_downloader --name semantic-segmentation-adas-0001 --precision FP16'),
             install_openvino_dependencies,
             download_picture('car_1.bmp'),
             bash(f'python3 {omz_python_demo_path} '
                  '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/'
                  'semantic-segmentation-adas-0001.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d CPU -at segmentation --no_show'),
             ],
            self.test_segmentation_python_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.parametrize('omz_python_demo_path', ['segmentation'], indirect=True)
    def test_segmentation_python_gpu(self, tester, image, omz_python_demo_path, bash,
                                     install_openvino_dependencies, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('omz_downloader --name semantic-segmentation-adas-0001 --precision FP16'),
             install_openvino_dependencies,
             download_picture('car_1.bmp'),
             bash(f'python3 {omz_python_demo_path} '
                  '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/'
                  'semantic-segmentation-adas-0001.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d GPU -at segmentation --no_show'),
             ],
            self.test_segmentation_python_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.parametrize('omz_python_demo_path', ['segmentation'], indirect=True)
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_segmentation_python_vpu(self, tester, image, omz_python_demo_path, bash, download_picture,
                                     install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('omz_downloader --name semantic-segmentation-adas-0001 --precision FP16'),
             download_picture('car_1.bmp'),
             bash(f'python3 {omz_python_demo_path} '
                  '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/'
                  'semantic-segmentation-adas-0001.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d MYRIAD -at segmentation --no_show'),
             ],
            self.test_segmentation_python_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.parametrize('omz_python_demo_path', ['segmentation'], indirect=True)
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_segmentation_python_hddl(self, tester, image, omz_python_demo_path, bash, download_picture,
                                      install_openvino_dependencies):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('omz_downloader --name semantic-segmentation-adas-0001 --precision FP16'),
             download_picture('car_1.bmp'),
             bash(f'umask 0000 && python3 {omz_python_demo_path} -at segmentation --no_show '
                  '-m /opt/intel/openvino/intel/semantic-segmentation-adas-0001/FP16/'
                  'semantic-segmentation-adas-0001.xml '
                  '-i /opt/intel/openvino/samples/car_1.bmp -d HDDL && rm -f /dev/shm/hddl_*'),
             ],
            self.test_segmentation_python_hddl.__name__, **kwargs,
        )
