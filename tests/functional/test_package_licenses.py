# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_not_image_os')
@pytest.mark.parametrize('_is_not_image_os', [('winserver2019', 'windows20h2')], indirect=True)
class TestLicenseLinux:
    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
    def test_package_licenses(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        kwargs = {
            'volumes': {
                root / 'logs' / image_folder / 'linux_deps': {'bind': '/tmp/logs'},  # nosec # noqa: S108
                root / 'tests' / 'resources' / 'linux_deps': {'bind': '/tmp/linux_deps'},  # nosec # noqa: S108
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "/tmp/linux_deps/package_licenses.sh"'],
            self.test_package_licenses.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_is_distribution')
    @pytest.mark.parametrize('_is_distribution', [('dev', 'dev_no_samples', 'proprietary')], indirect=True)
    def test_3d_party_dev_lin(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "test -f ./licensing/third-party-programs-docker-dev.txt"'],
            self.test_3d_party_dev_lin.__name__,
        )

    @pytest.mark.usefixtures('_is_distribution')
    @pytest.mark.parametrize('_is_distribution', [('runtime')], indirect=True)
    def test_3d_party_runtime_lin(self, tester, image):
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "test -f ./licensing/third-party-programs-docker-runtime.txt"'],
            self.test_3d_party_runtime_lin.__name__,
        )


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('winserver2019', 'windows20h2')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('runtime')], indirect=True)
class TestLicenseWindows:
    def test_3d_party_runtime_win(self, tester, image):
        kwargs = {'user': 'ContainerAdministrator'}
        tester.test_docker_image(
            image,
            ['cmd /S /C type C:\\\\intel\\\\openvino\\\\licensing\\\\third-party-programs-docker-runtime.txt'],
            self.test_3d_party_runtime_win.__name__, **kwargs,
        )
