# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Auxiliary structure for simplifying build process

Supports released/supported versions of product/its dependencies
"""
INTEL_OCL_RELEASE = {
    '20.03.15346': {
        'GMMLIB': '19.4.1',
        'IGC_CORE': '1.0.3151',
        'IGC_OPENCL': '1.0.3151',
        'INTEL_OPENCL': '20.03.15346',
        'INTEL_OCLOC': '20.03.15346',
    },
    '19.41.14441': {
        'GMMLIB': '19.3.2',
        'IGC_CORE': '1.0.2597',
        'IGC_OPENCL': '1.0.2597',
        'INTEL_OPENCL': '19.41.14441',
        'INTEL_OCLOC': '19.41.14441',
    },
    '19.04.12237': {
        'GMMLIB': '18.4.1',
        'IGC_CORE': '18.50.1270',
        'IGC_OPENCL': '18.50.1270',
        'INTEL_OPENCL': '19.04.12237',
        'INTEL_OCLOC': '19.04.12237',
    },
}
INTEL_OPENVINO_VERSION = {
    '2019.3': {
        'winserver2019':
            {
                'dev': '',
                'runtime': '',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16039/'
                               'w_openvino_toolkit_p_2019.3.379.exe',
            },
        'ubuntu18':
            {
                'dev': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16057/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2019.3.376.tgz',
                'runtime': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16057/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2019.3.376.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16057/'
                               'l_openvino_toolkit_p_2019.3.376.tgz',
            },
    },
    '2020.1': {
        'winserver2019':
            {
                'dev': '',
                'runtime': '',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16359/'
                               'w_openvino_toolkit_p_2020.1.033.exe',
            },
        'ubuntu18':
            {
                'dev': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16345/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.1.023_pot.tgz',
                'runtime': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16345/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.1.023.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16345/'
                               'l_openvino_toolkit_p_2020.1.023.tgz',
            },
    },
    '2020.2': {
        'winserver2019':
            {
                'dev': '',
                'runtime': '',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16613/'
                               'w_openvino_toolkit_p_2020.2.117.exe',
            },
        'ubuntu18':
            {
                'dev': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16612/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.2.120.tgz',
                'runtime': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16612/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.2.120.tgz',
                'proprietary': '',
                'data_dev': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16612/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2020.2.120.tgz',
            },
    },
    '2020.3': {
        'winserver2019':
            {
                'dev': '',
                'runtime': '',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16667/'
                               'w_openvino_toolkit_p_2020.3.194.exe',
            },
        'ubuntu18':
            {
                'dev': '',
                'runtime': '',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16670/'
                               'l_openvino_toolkit_p_2020.3.194.tgz',
                'data_dev': '',
            },
    },
    '2020.4': {
        'winserver2019':
            {
                'dev': '',
                'runtime': '',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16801/'
                               'w_openvino_toolkit_p_2020.4.287.exe',
            },
        'ubuntu18':
            {
                'dev': '',
                'runtime': '',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16803/'
                               'l_openvino_toolkit_p_2020.4.287.tgz',
                'data_dev': '',
            },
    },
}
DIVE_URL = {
    'windows': 'https://github.com/wagoodman/dive/releases/download/v0.9.2/dive_0.9.2_windows_amd64.zip',
}
SNYK_URL = {
    'windows': 'https://github.com/snyk/snyk/releases/download/v1.369.1/snyk-win.exe',
}
