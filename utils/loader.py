# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Auxiliary structure for simplifying build process

Supports released/supported versions of product/its dependencies
"""
INTEL_OCL_RELEASE = {
    '20.35.17767': {
        'GMMLIB': '20.2.4',
        'IGC_CORE': '1.0.4756',
        'IGC_OPENCL': '1.0.4756',
        'INTEL_OPENCL': '20.35.17767',
        'INTEL_OCLOC': '20.35.17767',
        'INTEL_ZERO': '1.0.17767',
    },
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
    '2020.1': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.1/'
                       'w_openvino_toolkit_dev_p_2020.1.033.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.1/'
                           'w_openvino_toolkit_runtime_p_2020.1.033.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16359/'
                               'w_openvino_toolkit_p_2020.1.033.exe',
            },
        'ubuntu18':
            {
                'dev': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16345/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.1.023_pot.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.1/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.1.023.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16345/'
                               'l_openvino_toolkit_p_2020.1.023.tgz',
            },
    },
    '2020.2': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.2/'
                       'w_openvino_toolkit_dev_p_2020.2.117.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.2/'
                           'w_openvino_toolkit_runtime_p_2020.2.117.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16613/'
                               'w_openvino_toolkit_p_2020.2.117.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.2/'
                            'w_openvino_toolkit_data_dev_p_2020.2.117.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.2/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.2.120.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.2/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.2.120.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16612/'
                               'l_openvino_toolkit_p_2020.2.120.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.2/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2020.2.120.tgz',
            },
    },
    '2020.3': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3/'
                       'w_openvino_toolkit_dev_p_2020.3.194.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3/'
                           'w_openvino_toolkit_runtime_p_2020.3.194.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16667/'
                               'w_openvino_toolkit_p_2020.3.194.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3/'
                            'w_openvino_toolkit_data_dev_p_2020.3.194.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.3.194.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.3.194.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16670/'
                               'l_openvino_toolkit_p_2020.3.194.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2020.3.194.tgz',
            },
    },
    '2020.3.1': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.1/'
                       'w_openvino_toolkit_dev_p_2020.3.341.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.1/'
                           'w_openvino_toolkit_runtime_p_2020.3.341.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17279/'
                               'w_openvino_toolkit_p_2020.3.341.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.1/'
                            'w_openvino_toolkit_data_dev_p_2020.3.341.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.1/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.3.341.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.1/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.3.341.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17276/'
                               'l_openvino_toolkit_p_2020.3.341.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.1/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2020.3.341.tgz',
            },
    },
    '2020.4': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.4/'
                       'w_openvino_toolkit_dev_p_2020.4.287.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.4/'
                           'w_openvino_toolkit_runtime_p_2020.4.287.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16801/'
                               'w_openvino_toolkit_p_2020.4.287.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.4/'
                            'w_openvino_toolkit_data_dev_p_2020.4.287.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.4/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.4.287.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.4/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.4.287.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/16803/'
                               'l_openvino_toolkit_p_2020.4.287.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.4/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2020.4.287.tgz',
            },
    },
    '2021.1': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                       'w_openvino_toolkit_dev_p_2021.1.110.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                           'w_openvino_toolkit_runtime_p_2021.1.110.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17063/'
                               'w_openvino_toolkit_p_2021.1.110.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                            'w_openvino_toolkit_data_dev_p_2021.1.110.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2021.1.110.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2021.1.110.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17062/'
                               'l_openvino_toolkit_p_2021.1.110.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2021.1.110.tgz',
            },
        'ubuntu20':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                           'l_openvino_toolkit_runtime_ubuntu20_p_2021.1.110.tgz',
            },
        'centos7':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/'
                           'l_openvino_toolkit_runtime_centos7_p_2021.1.110.tgz',
            },
    },
    '2021.2': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                       'w_openvino_toolkit_dev_p_2021.2.185.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                           'w_openvino_toolkit_runtime_p_2021.2.185.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17505/'
                               'w_openvino_toolkit_p_2021.2.185.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                            'w_openvino_toolkit_data_dev_p_2021.2.185.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2021.2.185.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2021.2.185.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17504/'
                               'l_openvino_toolkit_p_2021.2.185.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2021.2.185.tgz',
            },
        'ubuntu20':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                           'l_openvino_toolkit_runtime_ubuntu20_p_2021.2.185.tgz',
            },
        'centos7':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                           'l_openvino_toolkit_runtime_centos7_p_2021.2.185.tgz',
            },
        'rhel8':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.2/'
                           'l_openvino_toolkit_runtime_rhel8_p_2021.2.185.tgz',
            },
    },
}
DIVE_URL = {
    'windows': 'https://github.com/wagoodman/dive/releases/download/v0.9.2/dive_0.9.2_windows_amd64.zip',
}
SNYK_URL = {
    'windows': 'https://github.com/snyk/snyk/releases/download/v1.413.4/snyk-win.exe',
}
