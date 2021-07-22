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

        env_template_file_name = f'{distribution}_env.dockerfile.j2'
        expected_env_file_path = root / 'templates' / image_os / 'dist' / env_template_file_name

        kwargs = {
            'volumes': {
                log_folder: {'bind': '/tmp/logs', 'mode': 'rw'},  # nosec # noqa: S108
                expected_env_file_path.parent: {'bind': '/tmp/dist', 'mode': 'rw'},  # nosec # noqa: S108

                # temp
                root / 'tests' / 'resources' / 'linux_deps':
                    {'bind': '/tmp/linux_deps', 'mode': 'rw'},  # nosec # noqa: S108
            },

        }
        tester.test_docker_image(
            image,
            ["/bin/bash -c 'OLD_ENV=$(env | sort) && "
             'source /opt/intel/openvino/bin/setupvars.sh > /dev/null && '
             'NEW_ENV=$(env | sort) && '
             f'comm -13 <(echo -ne "$OLD_ENV") <(echo -ne "$NEW_ENV") | sed -e "s/^/ENV /" | '
             f"tee /tmp/logs/{env_template_file_name}'",
             f'/bin/bash -ac "python3 /tmp/linux_deps/linux_deps_compare.py -i {image} '
             f'-e /tmp/dist/{env_template_file_name} '
             f'-c /tmp/logs/{env_template_file_name} -l /tmp/logs"',
             ],
            self.test_setupvars_changes_linux.__name__, **kwargs,
        )
