# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
class TestToolsLinux:
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev')], indirect=True)
    def test_accuracy_checker(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('accuracy_check -h')],
            self.test_accuracy_checker.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev')], indirect=True)
    def test_benchmark(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('benchmark_app -h')],
            self.test_benchmark.__name__, **kwargs,
        )

    @pytest.mark.skip(reason='cl_compiler is not present in 2022.3')
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('runtime', 'dev')], indirect=True)
    def test_cl_compiler(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('cd /opt/intel/openvino/tools/cl_compiler/bin && '
                  './clc -h')],
            self.test_cl_compiler.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('runtime', 'dev')], indirect=True)
    def test_compile_tool(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('cd /opt/intel/openvino/tools/compile_tool && '
                  './compile_tool -h')],
            self.test_compile_tool.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev')], indirect=True)
    def test_deployment_manager(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('cd /opt/intel/openvino/tools/deployment_manager && '
                  'python3 deployment_manager.py -h')],
            self.test_deployment_manager.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev')], indirect=True)
    def test_mo(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('mo --help')],
            self.test_mo.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev')], indirect=True)
    def test_omz(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('omz_converter --help'),
             bash('omz_data_downloader --help'),
             bash('omz_downloader --help'),
             bash('omz_info_dumper --help'),
             bash('omz_quantizer --help'),
             ],
            self.test_omz.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev')], indirect=True)
    def test_pot(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('pot --help')],
            self.test_pot.__name__, **kwargs,
        )
