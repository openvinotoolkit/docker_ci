# -*- coding: utf-8 -*-
# Copyright (C) 2019-2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Auxiliary structure for simplifying build process

Supports released/supported versions of product/its dependencies
"""
INTEL_OPENVINO_VERSION = {
    '2023.0.0': {
        'ubuntu22':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                       'linux/l_openvino_toolkit_ubuntu22_2023.0.0.10926.b4452d56304_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                           'linux/l_openvino_toolkit_ubuntu22_2023.0.0.10926.b4452d56304_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                       'linux/l_openvino_toolkit_rhel8_2023.0.0.10926.b4452d56304_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                           'linux/l_openvino_toolkit_rhel8_2023.0.0.10926.b4452d56304_x86_64.tgz',
            },
    },
    '2023.2.0': {
        'ubuntu22':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.2/'
                       'linux/l_openvino_toolkit_ubuntu22_2023.2.0.13089.cfd42bd2cb0_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.2/'
                           'linux/l_openvino_toolkit_ubuntu22_2023.2.0.13089.cfd42bd2cb0_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.2/'
                       'linux/l_openvino_toolkit_rhel8_2023.2.0.13089.cfd42bd2cb0_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.2/'
                           'linux/l_openvino_toolkit_rhel8_2023.2.0.13089.cfd42bd2cb0_x86_64.tgz',
            },
    },
    '2023.3.0': {
        'ubuntu22':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.3/'
                       'linux/l_openvino_toolkit_ubuntu22_2023.3.0.13775.ceeafaf64f3_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.3/'
                           'linux/l_openvino_toolkit_ubuntu22_2023.3.0.13775.ceeafaf64f3_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.3/'
                       'linux/l_openvino_toolkit_rhel8_2023.3.0.13775.ceeafaf64f3_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.3/'
                           'linux/l_openvino_toolkit_rhel8_2023.3.0.13775.ceeafaf64f3_x86_64.tgz',
            },
    },
    '2024.0.0': {
        'ubuntu22':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.0/'
                       'linux/l_openvino_toolkit_ubuntu22_2024.0.0.14509.34caeefd078_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.0/'
                           'linux/l_openvino_toolkit_ubuntu22_2024.0.0.14509.34caeefd078_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.0/'
                       'linux/l_openvino_toolkit_rhel8_2024.0.0.14509.34caeefd078_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.0/'
                           'linux/l_openvino_toolkit_rhel8_2024.0.0.14509.34caeefd078_x86_64.tgz',
            },
    },
    '2024.1.0': {
        'ubuntu22': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.1/'
                   'linux/l_openvino_toolkit_ubuntu22_2024.1.0.15008.f4afc983258_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.1/'
                   'linux/l_openvino_toolkit_ubuntu22_2024.1.0.15008.f4afc983258_x86_64.tgz',
        },
        'rhel8': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.1/'
                   'linux/l_openvino_toolkit_rhel8_2024.1.0.15008.f4afc983258_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.1/'
                   'linux/l_openvino_toolkit_rhel8_2024.1.0.15008.f4afc983258_x86_64.tgz',
        },
    },
    '2024.2.0': {
        'ubuntu22': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.2/'
                   'linux/l_openvino_toolkit_ubuntu22_2024.2.0.15519.5c0f38f83f6_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.2/'
                       'linux/l_openvino_toolkit_ubuntu22_2024.2.0.15519.5c0f38f83f6_x86_64.tgz',
        },
        'rhel8': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.2/'
                   'linux/l_openvino_toolkit_rhel8_2024.2.0.15519.5c0f38f83f6_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.2/'
                       'linux/l_openvino_toolkit_rhel8_2024.2.0.15519.5c0f38f83f6_x86_64.tgz',
        },
    },
    '2024.3.0': {
        'ubuntu22': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.3/linux/'
                   'l_openvino_toolkit_ubuntu22_2024.3.0.16041.1e3b88e4e3f_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.3/linux/'
                       'l_openvino_toolkit_ubuntu22_2024.3.0.16041.1e3b88e4e3f_x86_64.tgz',
        },
        'rhel8': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.3/linux/'
                   'l_openvino_toolkit_rhel8_2024.3.0.16041.1e3b88e4e3f_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.3/linux/'
                       'l_openvino_toolkit_rhel8_2024.3.0.16041.1e3b88e4e3f_x86_64.tgz',
        },
    },
    '2024.4.0': {
        'ubuntu22': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                   '2024.4/linux/openvino_genai_ubuntu22_2024.4.0.0_x86_64.tar.gz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                       '2024.4/linux/openvino_genai_ubuntu22_2024.4.0.0_x86_64.tar.gz',
        },
        'rhel8': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                   '2024.4/linux/l_openvino_toolkit_rhel8_2024.4.0.16579.c3152d32c9c_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                       '2024.4/linux/l_openvino_toolkit_rhel8_2024.4.0.16579.c3152d32c9c_x86_64.tgz',
        },
    },
    '2024.5.0': {
        'ubuntu22': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                   '2024.5/linux/openvino_genai_ubuntu22_2024.5.0.0_x86_64.tar.gz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                       '2024.5/linux/openvino_genai_ubuntu22_2024.5.0.0_x86_64.tar.gz',
        },
        'ubuntu24': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                   '2024.5/linux/openvino_genai_ubuntu24_2024.5.0.0_x86_64.tar.gz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                       '2024.5/linux/openvino_genai_ubuntu24_2024.5.0.0_x86_64.tar.gz',
        },
        'rhel8': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                   '2024.5/linux/l_openvino_toolkit_rhel8_2024.5.0.17288.7975fa5da0c_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                       '2024.5/linux/l_openvino_toolkit_rhel8_2024.5.0.17288.7975fa5da0c_x86_64.tgz',
        },
    },
    '2024.6.0': {
        'ubuntu22': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                   '2024.6/linux/openvino_genai_ubuntu22_2024.6.0.0_x86_64.tar.gz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                       '2024.6/linux/openvino_genai_ubuntu22_2024.6.0.0_x86_64.tar.gz',
        },
        'ubuntu24': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                   '2024.6/linux/openvino_genai_ubuntu24_2024.6.0.0_x86_64.tar.gz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                       '2024.6/linux/openvino_genai_ubuntu24_2024.6.0.0_x86_64.tar.gz',
        },
        'rhel8': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                   '2024.6/linux/l_openvino_toolkit_rhel8_2024.6.0.17404.4c0f47d2335_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                       '2024.6/linux/l_openvino_toolkit_rhel8_2024.6.0.17404.4c0f47d2335_x86_64.tgz',
        },
    },
    "2025.0.0": {
        'ubuntu22': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                   '2025.0/linux/openvino_genai_ubuntu22_2025.0.0.0_x86_64.tar.gz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                       '2025.0/linux/openvino_genai_ubuntu22_2025.0.0.0_x86_64.tar.gz',
        },
        'ubuntu24': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                   '2025.0/linux/openvino_genai_ubuntu24_2025.0.0.0_x86_64.tar.gz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino_genai/packages/'
                       '2025.0/linux/openvino_genai_ubuntu24_2025.0.0.0_x86_64.tar.gz',
        },
        'rhel8': {
            'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                   '2025.0/linux/openvino_toolkit_rhel8_2025.0.0.17942.1f68be9f594_x86_64.tgz',
            'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/'
                       '2025.0/linux/openvino_toolkit_rhel8_2025.0.0.17942.1f68be9f594_x86_64.tgz',
        },
    }
}
DIVE_URL = {
    'windows': 'https://github.com/wagoodman/dive/releases/download/v0.9.2/dive_0.9.2_windows_amd64.zip',
}
SNYK_URL = {
    'windows': 'https://github.com/snyk/snyk/releases/download/v1.658.0/snyk-win.exe',
}
