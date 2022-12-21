# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Auxiliary structure for simplifying build process

Supports released/supported versions of product/its dependencies
"""
INTEL_OPENVINO_VERSION = {
    '2022.3.0': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'windows/w_openvino_toolkit_windows_2022.3.0.9052.9752fafe8eb_x86_64.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'windows/w_openvino_toolkit_windows_2022.3.0.9052.9752fafe8eb_x86_64.zip',
            },
        'windows20h2':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'windows/w_openvino_toolkit_windows_2022.3.0.9052.9752fafe8eb_x86_64.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'windows/w_openvino_toolkit_windows_2022.3.0.9052.9752fafe8eb_x86_64.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'linux/l_openvino_toolkit_ubuntu18_2022.3.0.9052.9752fafe8eb_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3'
                       'linux/l_openvino_toolkit_ubuntu18_2022.3.0.9052.9752fafe8eb_x86_64.tgz',
            },
        'ubuntu20':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'linux/l_openvino_toolkit_ubuntu20_2022.3.0.9052.9752fafe8eb_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'linux/l_openvino_toolkit_ubuntu20_2022.3.0.9052.9752fafe8eb_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'linux/l_openvino_toolkit_rhel8_2022.3.0.9052.9752fafe8eb_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
                       'linux/l_openvino_toolkit_rhel8_2022.3.0.9052.9752fafe8eb_x86_64.tgz',
            },
    },
}
DIVE_URL = {
    'windows': 'https://github.com/wagoodman/dive/releases/download/v0.9.2/dive_0.9.2_windows_amd64.zip',
}
SNYK_URL = {
    'windows': 'https://github.com/snyk/snyk/releases/download/v1.658.0/snyk-win.exe',
}
