# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Auxiliary structure for simplifying build process

Supports released/supported versions of product/its dependencies
"""
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
    '2020.3.2': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.2/'
                       'w_openvino_toolkit_dev_p_2020.3.355.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.2/'
                           'w_openvino_toolkit_runtime_p_2020.3.355.zip',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17804/'
                               'w_openvino_toolkit_p_2020.3.355.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.2/'
                            'w_openvino_toolkit_data_dev_p_2020.3.355.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.2/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2020.3.355.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.2/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2020.3.355.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17805/'
                               'l_openvino_toolkit_p_2020.3.355.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.2/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2020.3.355.tgz',
            },
        'centos7':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2020.3.2/'
                           'l_openvino_toolkit_runtime_centos7_p_2020.3.355.tgz',
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
    '2021.3': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                       'w_openvino_toolkit_dev_p_2021.3.394.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                           'w_openvino_toolkit_runtime_p_2021.3.394.zip',
                'proprietary': 'https://registrationcenter-download.intel.com/akdlm/irc_nas/17661/'
                               'w_openvino_toolkit_p_2021.3.394.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                            'w_openvino_toolkit_data_dev_p_2021.3.394.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2021.3.394.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2021.3.394.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17662/'
                               'l_openvino_toolkit_p_2021.3.394.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2021.3.394.tgz',
            },
        'ubuntu20':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                       'l_openvino_toolkit_dev_ubuntu20_p_2021.3.394.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                           'l_openvino_toolkit_runtime_ubuntu20_p_2021.3.394.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                            'l_openvino_toolkit_data_dev_ubuntu20_p_2021.3.394.tgz',
            },
        'centos7':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                           'l_openvino_toolkit_runtime_centos7_p_2021.3.394.tgz',
            },
        'rhel8':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.3/'
                           'l_openvino_toolkit_runtime_rhel8_p_2021.3.394.tgz',
            },
    },
    '2021.4': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                       'w_openvino_toolkit_dev_p_2021.4.582.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                           'w_openvino_toolkit_runtime_p_2021.4.582.zip',
                'proprietary': 'https://registrationcenter-download.intel.com/akdlm/irc_nas/17987/'
                               'w_openvino_toolkit_p_2021.4.582.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                            'w_openvino_toolkit_data_dev_p_2021.4.582.zip',
            },
        'windows20h2':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                       'w_openvino_toolkit_dev_p_2021.4.582.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                           'w_openvino_toolkit_runtime_p_2021.4.582.zip',
                'proprietary': 'https://registrationcenter-download.intel.com/akdlm/irc_nas/17987/'
                               'w_openvino_toolkit_p_2021.4.582.exe',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                            'w_openvino_toolkit_data_dev_p_2021.4.582.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2021.4.582.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2021.4.582.tgz',
                'proprietary': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/17988/'
                               'l_openvino_toolkit_p_2021.4.582.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                            'l_openvino_toolkit_data_dev_ubuntu18_p_2021.4.582.tgz',
            },
        'ubuntu20':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                       'l_openvino_toolkit_dev_ubuntu20_p_2021.4.582.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                           'l_openvino_toolkit_runtime_ubuntu20_p_2021.4.582.tgz',
                'data_dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                            'l_openvino_toolkit_data_dev_ubuntu20_p_2021.4.582.tgz',
            },
        'centos7':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                           'l_openvino_toolkit_runtime_centos7_p_2021.4.582.tgz',
            },
        'rhel8':
            {
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/'
                           'l_openvino_toolkit_runtime_rhel8_p_2021.4.582.tgz',
            },
    },
    '2022.1.0': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                       'w_openvino_toolkit_dev_p_2022.1.0.643.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                           'w_openvino_toolkit_runtime_p_2022.1.0.643.zip',
            },
        'windows20h2':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                       'w_openvino_toolkit_dev_p_2022.1.0.643.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                           'w_openvino_toolkit_runtime_p_2022.1.0.643.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                       'l_openvino_toolkit_dev_ubuntu18_p_2022.1.0.643.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                           'l_openvino_toolkit_runtime_ubuntu18_p_2022.1.0.643.tgz',
            },
        'ubuntu20':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                       'l_openvino_toolkit_dev_ubuntu20_p_2022.1.0.643.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                           'l_openvino_toolkit_runtime_ubuntu20_p_2022.1.0.643.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                       'l_openvino_toolkit_dev_rhel8_p_2022.1.0.643.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.1/'
                           'l_openvino_toolkit_runtime_rhel8_p_2022.1.0.643.tgz',
            },
    },
    '2022.2.0': {
        'winserver2019':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'windows/w_openvino_toolkit_windows_2022.2.0.7713.af16ea1d79a_x86_64.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'windows/w_openvino_toolkit_windows_2022.2.0.7713.af16ea1d79a_x86_64.zip',
            },
        'windows20h2':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'windows/w_openvino_toolkit_windows_2022.2.0.7713.af16ea1d79a_x86_64.zip',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'windows/w_openvino_toolkit_windows_2022.2.0.7713.af16ea1d79a_x86_64.zip',
            },
        'ubuntu18':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'linux/l_openvino_toolkit_ubuntu18_2022.2.0.7713.af16ea1d79a_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'linux/l_openvino_toolkit_ubuntu18_2022.2.0.7713.af16ea1d79a_x86_64.tgz',
            },
        'ubuntu20':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'linux/l_openvino_toolkit_ubuntu20_2022.2.0.7713.af16ea1d79a_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'linux/l_openvino_toolkit_ubuntu20_2022.2.0.7713.af16ea1d79a_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'linux/l_openvino_toolkit_rhel8_2022.2.0.7713.af16ea1d79a_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/'
                       'linux/l_openvino_toolkit_rhel8_2022.2.0.7713.af16ea1d79a_x86_64.tgz',
            },
    },
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
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/'
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
    '2023.0.0': {
        'ubuntu22':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                'linux/l_openvino_toolkit_ubuntu22_2023.0.0.10926.b4452d56304_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                'linux/l_openvino_toolkit_ubuntu22_2023.0.0.10926.b4452d56304_x86_64.tgz',
            },
        'ubuntu20':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                'linux/l_openvino_toolkit_ubuntu20_2023.0.0.10926.b4452d56304_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                'linux/l_openvino_toolkit_ubuntu20_2023.0.0.10926.b4452d56304_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                'linux/l_openvino_toolkit_rhel8_2023.0.0.10926.b4452d56304_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/'
                'linux/l_openvino_toolkit_rhel8_2023.0.0.10926.b4452d56304_x86_64.tgz',
            },
    },
    '2023.1.0': {
        'ubuntu22':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.1/'
                'linux/l_openvino_toolkit_ubuntu22_2023.1.0.12185.47b736f63ed_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.1/'
                'linux/l_openvino_toolkit_ubuntu22_2023.1.0.12185.47b736f63ed_x86_64.tgz',
            },
        'ubuntu20':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.1/'
                'linux/l_openvino_toolkit_ubuntu20_2023.1.0.12185.47b736f63ed_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.1/'
                'linux/l_openvino_toolkit_ubuntu20_2023.1.0.12185.47b736f63ed_x86_64.tgz',
            },
        'rhel8':
            {
                'dev': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.1/'
                'linux/l_openvino_toolkit_rhel8_2023.1.0.12185.47b736f63ed_x86_64.tgz',
                'runtime': 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.1/'
                'linux/l_openvino_toolkit_rhel8_2023.1.0.12185.47b736f63ed_x86_64.tgz',
            },
    },
}
DIVE_URL = {
    'windows': 'https://github.com/wagoodman/dive/releases/download/v0.9.2/dive_0.9.2_windows_amd64.zip',
}
SNYK_URL = {
    'windows': 'https://github.com/snyk/snyk/releases/download/v1.658.0/snyk-win.exe',
}
