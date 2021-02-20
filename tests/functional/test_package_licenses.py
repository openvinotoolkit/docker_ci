# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_image_os')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
def test_package_licenses(tester, image):
    root = pathlib.Path(os.path.realpath(__name__)).parent
    image_folder = image.replace('/', '_').replace(':', '_')
    kwargs = {
        'volumes': {
            root / 'logs' / image_folder / 'linux_deps': {'bind': '/tmp/logs'},  # nosec
            root / 'tests' / 'resources' / 'linux_deps': {'bind': '/tmp/linux_deps'},  # nosec
        },
    }
    tester.test_docker_image(
        image,
        ['/bin/bash -ac "chmod +x /tmp/linux_deps/package_licenses.sh && '
         '/tmp/linux_deps/package_licenses.sh"'],
        test_package_licenses.__name__, **kwargs,
    )
