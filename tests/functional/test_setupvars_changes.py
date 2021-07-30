# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest


@pytest.mark.usefixtures('_is_image_os', '_is_not_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'centos7', 'rhel8')], indirect=True)
@pytest.mark.parametrize('_is_not_distribution', [('base', 'custom-no-omz', 'custom-no-cv',
                                                   'custom-full')], indirect=True)
class TestSetupvarsChanges:
    def test_setupvars_changes_linux(self, tester, image, image_os, distribution):
        root = pathlib.Path(os.path.realpath(__name__)).parent
        image_folder = image.replace('/', '_').replace(':', '_')
        log_folder = root / 'logs' / image_folder / 'environment_vars'
        if not log_folder.exists():
            log_folder.mkdir(parents=True)
        expected_env_file_path = root / 'templates' / image_os / 'env'

        kwargs = {
            'volumes': {
                log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec # noqa: S108
                expected_env_file_path: {'bind': '/tmp/dist', 'mode': 'rw'},  # nosec # noqa: S108

                # temp
                root / 'tests' / 'resources' / 'environment_vars':
                    {'bind': '/tmp/environment_vars', 'mode': 'rw'},  # nosec # noqa: S108
            },

        }
        tester.test_docker_image(
            image,
            ["/bin/bash -c 'env > /tmp/logs/env_setupvars_before.txt && "
             'source /opt/intel/openvino/bin/setupvars.sh > /dev/null && '
             "env > /tmp/logs/env_setupvars_after.txt'",
             '/bin/bash -ac "python3 /tmp/environment_vars/env_vars_changes_compare.py '
             f'-e /tmp/dist/{distribution}_env.dockerfile.j2 '
             '-b /tmp/logs/env_setupvars_before.txt -a /tmp/logs/env_setupvars_after.txt '
             f'-c /tmp/environment_vars/{image_os}_env.json '
             f'-i {image} -os {image_os} -dist {distribution} -l /tmp/logs"',
             ],
            self.test_setupvars_changes_linux.__name__, **kwargs,
        )
