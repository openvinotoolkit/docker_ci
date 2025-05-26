# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest

from utils.exceptions import FailedTestError


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'ubuntu22', 'rhel8')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'custom-full')], indirect=True)
class TestSamplesLinux:
    def test_benchmark_app_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name squeezenet1.1 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('omz_converter --name squeezenet1.1 --precisions FP16 '
                  '-d /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car.png'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/benchmark_app -pc -niter 1000 -m '
                  '/root/openvino_cpp_samples_build/intel64/Release/public/squeezenet1.1/FP16/squeezenet1.1.xml'
                  ' -i /opt/intel/openvino/samples/car.png -d CPU'),
             ], self.test_benchmark_app_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_benchmark_app_cpp_gpu(self, tester, image, gpu_kwargs, install_openvino_dependencies, bash,
                                   download_picture):
        kwargs = dict(mem_limit='3g', **gpu_kwargs)
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name squeezenet1.1 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('omz_converter --name squeezenet1.1 --precisions FP16 '
                  '-d /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car.png'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/benchmark_app -pc -niter 1000 -m '
                  '/root/openvino_cpp_samples_build/intel64/Release/public/squeezenet1.1/FP16/squeezenet1.1.xml'
                  ' -i /opt/intel/openvino/samples/car.png -d GPU'),
             ], self.test_benchmark_app_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_benchmark_app_cpp_vpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name squeezenet1.1 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('omz_converter --name squeezenet1.1 --precisions FP16 '
                  '-d /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car.png'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/benchmark_app -pc -niter 1000 -m '
                  '/root/openvino_cpp_samples_build/intel64/Release/public/squeezenet1.1/FP16/squeezenet1.1.xml'
                  ' -i /opt/intel/openvino/samples/car.png -d MYRIAD'),
             ], self.test_benchmark_app_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_benchmark_app_cpp_hddl(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name squeezenet1.1 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('omz_converter --name squeezenet1.1 --precisions FP16 '
                  '-d /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car.png'),
             bash('umask 0000 && /root/openvino_cpp_samples_build/intel64/Release/benchmark_app '
                  '-m /root/openvino_cpp_samples_build/intel64/Release/public/'
                  'squeezenet1.1/FP16/squeezenet1.1.xml -i /opt/intel/openvino/samples/car.png -pc -niter 1000 '
                  '-d HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_benchmark_app_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_hello_classification_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/car_1.bmp CPU'),
             ], self.test_hello_classification_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_hello_classification_cpp_gpu(self, tester, image, gpu_kwargs, install_openvino_dependencies, bash,
                                          download_picture):
        kwargs = dict(mem_limit='3g', **gpu_kwargs)
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/car_1.bmp GPU'),
             ], self.test_hello_classification_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_classification_cpp_vpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/car_1.bmp MYRIAD'),
             ], self.test_hello_classification_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_classification_cpp_hddl(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('umask 0000 && /root/openvino_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/car_1.bmp HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_hello_classification_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_min_product_version')
    @pytest.mark.parametrize('_min_product_version', ['2021.2'], indirect=True)
    def test_hello_classification_cpp_fail(self, tester, image, caplog, bash,
                                           install_openvino_dependencies, download_picture):
        with pytest.raises(FailedTestError):
            tester.test_docker_image(
                image,
                [install_openvino_dependencies,
                 bash('cd /opt/intel/openvino/samples/cpp && '
                      '/opt/intel/openvino/samples/cpp/build_samples.sh'),
                 bash('omz_downloader --name vehicle-attributes-recognition-barrier-0039 --precisions FP32 '
                      '-o /root/openvino_cpp_samples_build/intel64/Release/'),
                 download_picture('car.png'),
                 bash('/root/openvino_cpp_samples_build/intel64/Release/hello_classification '
                      '/root/openvino_cpp_samples_build/intel64/Release/intel/'
                      'vehicle-attributes-recognition-barrier-0039/FP32/'
                      'vehicle-attributes-recognition-barrier-0039.xml '
                      '/opt/intel/openvino/samples/car.png CPU'),
                 ], self.test_hello_classification_cpp_fail.__name__,
            )
        if 'Sample supports models with 1 output only' not in caplog.text:
            pytest.fail('Sample supports models with 1 output only')

    def test_hello_reshape_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/openvino_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/car_1.bmp CPU'),
             ], self.test_hello_reshape_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_hello_reshape_cpp_gpu(self, tester, image, gpu_kwargs, install_openvino_dependencies, bash,
                                   download_picture):
        kwargs = dict(mem_limit='3g', **gpu_kwargs)
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/openvino_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/car_1.bmp GPU'),
             ], self.test_hello_reshape_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_reshape_cpp_vpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/openvino_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/car_1.bmp MYRIAD'),
             ], self.test_hello_reshape_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_reshape_cpp_hddl(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('umask 0000 && /root/openvino_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/openvino_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/car_1.bmp HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_hello_reshape_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_classification_async_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('python3 -c \\"import cv2; '
                  "img = cv2.imread('/opt/intel/openvino/samples/car_1.bmp', cv2.IMREAD_UNCHANGED); "
                  'res = cv2.resize(img, (227,227)); '
                  'cv2.imwrite(\'/opt/intel/openvino/samples/car_1_227.bmp\', res)\\"'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/car_1_227.bmp -d CPU'),
             ], self.test_classification_async_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_classification_async_cpp_gpu(self, tester, image, gpu_kwargs, install_openvino_dependencies, bash,
                                          download_picture):
        kwargs = dict(mem_limit='3g', **gpu_kwargs)
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('python3 -c \\"import cv2; '
                  "img = cv2.imread('/opt/intel/openvino/samples/car_1.bmp', cv2.IMREAD_UNCHANGED); "
                  'res = cv2.resize(img, (227,227)); '
                  'cv2.imwrite(\'/opt/intel/openvino/samples/car_1_227.bmp\', res)\\"'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/car_1_227.bmp -d GPU'),
             ], self.test_classification_async_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_classification_async_cpp_vpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('python3 -c \\"import cv2; '
                  "img = cv2.imread('/opt/intel/openvino/samples/car_1.bmp', cv2.IMREAD_UNCHANGED); "
                  'res = cv2.resize(img, (227,227)); '
                  'cv2.imwrite(\'/opt/intel/openvino/samples/car_1_227.bmp\', res)\\"'),
             bash('/root/openvino_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/car_1_227.bmp -d MYRIAD'),
             ], self.test_classification_async_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_classification_async_cpp_hddl(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/openvino_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/openvino_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/openvino_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('python3 -c \\"import cv2; '
                  "img = cv2.imread('/opt/intel/openvino/samples/car_1.bmp', cv2.IMREAD_UNCHANGED); "
                  'res = cv2.resize(img, (227,227)); '
                  'cv2.imwrite(\'/opt/intel/openvino/samples/car_1_227.bmp\', res)\\"'),
             bash('umask 0000 && /root/openvino_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/openvino_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/car_1_227.bmp -d HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_classification_async_cpp_hddl.__name__, **kwargs,
        )
