# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
class TestToolsLinux:
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_accuracy_checker(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('accuracy_check -h')],
            self.test_accuracy_checker.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_benchmark(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('cd /opt/intel/openvino/tools/benchmark_tool && '
                  'python3 benchmark_app.py -h')],
            self.test_benchmark.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('runtime', 'dev', 'proprietary')], indirect=True)
    def test_cl_compiler(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('cd /opt/intel/openvino/tools/cl_compiler/bin && '
                  './clc -h')],
            self.test_cl_compiler.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('runtime', 'dev', 'proprietary')], indirect=True)
    def test_compile_tool(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('cd /opt/intel/openvino/tools/compile_tool && '
                  './compile_tool -h')],
            self.test_compile_tool.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_deployment_manager(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('cd /opt/intel/openvino/tools/deployment_manager && '
                  'python3 deployment_manager.py -h')],
            self.test_deployment_manager.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_pot(self, tester, image, bash):
        kwargs = {'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [bash('pot --help')],
            self.test_pot.__name__, **kwargs,
        )
