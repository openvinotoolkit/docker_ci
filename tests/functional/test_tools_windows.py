# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019', 'windows20h2')], indirect=True)
class TestToolsWindows:
    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_accuracy_checker(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['accuracy_check -h'],
            self.test_accuracy_checker.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_benchmark(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['benchmark_app -h'],
            self.test_benchmark.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('runtime', 'dev', 'proprietary')], indirect=True)
    def test_compile_tool(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\tools\\\\compile_tool\\\\ && '
             'compile_tool -h'],
            self.test_compile_tool.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_deployment_manager(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'cd C:\\\\intel\\\\openvino\\\\tools\\\\deployment_manager\\\\ && '
             'python deployment_manager.py -h'],
            self.test_deployment_manager.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_mo(self, tester, image, bash):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['mo --help'],
            self.test_mo.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_omz(self, tester, image, bash):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['omz_converter --help',
             'omz_data_downloader --help',
             'omz_downloader --help',
             'omz_info_dumper --help',
             'omz_quantizer --help',
             ],
            self.test_omz.__name__, **kwargs,
        )

    @pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary')], indirect=True)
    def test_pot(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['pot --help'],
            self.test_pot.__name__, **kwargs,
        )
