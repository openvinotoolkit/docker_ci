# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019')], indirect=True)
class TestToolsWindows:
    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_accuracy_checker(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'accuracy_check -h'],
            self.test_accuracy_checker.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_benchmark(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\tools\\\\benchmark_tool\\\\ && '
             'python benchmark_app.py -h'],
            self.test_benchmark.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('runtime', 'dev', 'proprietary')], indirect=True)
    def test_compile_tool(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\tools\\\\compile_tool\\\\ && '
             'compile_tool -h'],
            self.test_compile_tool.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_cross_check_tool(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\tools\\\\cross_check_tool\\\\ && '
             'python cross_check_tool.py -h'],
            self.test_cross_check_tool.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_deployment_manager(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\deployment_tools\\\\tools\\\\deployment_manager\\\\ && '
             'python deployment_manager.py -h'],
            self.test_deployment_manager.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_pot(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\bin\\\\setupvars.bat && '
             'pot --help'],
            self.test_pot.__name__, **kwargs,
        )
