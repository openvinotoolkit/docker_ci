# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_not_distribution')
@pytest.mark.parametrize('_is_not_distribution', [('base')], indirect=True)
class TestLinuxDependencies:
    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20')], indirect=True)
    def test_gpl_apt_deps(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        log_folder = root / 'logs' / image_folder / 'linux_deps'
        if not log_folder.exists():
            log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'linux_deps':
                    {'bind': '/tmp/linux_deps', 'mode': 'rw'},  # nosec # noqa: S108
                log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec # noqa: S108
            },
        }
        # dpkg has no standard way to get licenses of installed packages
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "dpkg-query --show -f=\'${Package} ${Version}\n\' 2>&1 | tee /tmp/logs/apt_deps.log"',
             '/bin/bash -ac "apt-cache depends --no-recommends --no-suggests --no-enhances '
             '$(dpkg-query --show -f=\'${Package} \') 2>&1 | tee /tmp/logs/apt_deps_tree.log"',
             '/bin/bash -ac "python3 /tmp/linux_deps/search_gpl_packages.py -f /tmp/logs/apt_deps.log -p apt '
             '-w /thirdparty/base_packages.txt -l /tmp/logs/gpl_packages.log"',
             ],
            self.test_gpl_apt_deps.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_is_image_os')
    @pytest.mark.parametrize('_is_image_os', [('rhel8')], indirect=True)
    def test_gpl_yum_deps(self, tester, image):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        log_folder = root / 'logs' / image_folder / 'linux_deps'
        if not log_folder.exists():
            log_folder.mkdir(parents=True)
        kwargs = {
            'volumes': {
                root / 'tests' / 'resources' / 'linux_deps':
                    {'bind': '/tmp/linux_deps', 'mode': 'rw'},  # nosec # noqa: S108
                log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec # noqa: S108
            },
        }
        tester.test_docker_image(
            image,
            ['/bin/bash -ac "rpm -qa --qf \'%{name}:%{version}:%{license}\n\' | column -t -s \':\' 2>&1 '
             '| tee /tmp/logs/yum_deps.log"',
             '/bin/bash -ac "for i in $(rpm -qa --qf \'%{name} \'); '
             'do echo \\\"Dependencies of $i:\\\"; rpm -qR $i | '
             'sed \'s/^/  /\'; done 2>&1 | tee /tmp/logs/yum_deps_tree.log"',
             'python3 /tmp/linux_deps/search_gpl_packages.py -f /tmp/logs/yum_deps.log -p yum '
             '-w /thirdparty/base_packages.txt -l /tmp/logs/gpl_packages.log',
             ],
            self.test_gpl_yum_deps.__name__, **kwargs,
        )
