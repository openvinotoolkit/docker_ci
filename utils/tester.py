# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Module that handles running tests on Docker image"""
import logging
import pathlib
import typing

from docker.errors import APIError
from docker.models.containers import Container
from docker.models.images import Image

from utils import logger
from utils.docker_api import DockerAPI
from utils.exceptions import FailedTest
from utils.utilities import get_system_proxy

log = logging.getLogger('docker_ci')


class DockerImageTester(DockerAPI):
    """Wrapper for docker.api.client implementing custom docker.image.run execution and logging"""

    def __init__(self):
        super().__init__()
        self.container: typing.Optional[Container] = None
        log.setLevel(logging.DEBUG)

    def test_docker_image(self,
                          image: typing.Tuple[Image, str],
                          commands: typing.List[str], test_name: str,
                          is_cached: bool = False, **kwargs: typing.Optional[typing.Dict]):
        """Running list of commands inside the container, logging the output and handling possible exceptions"""
        if isinstance(image, Image):
            file_tag = image.tags[0].replace('/', '_').replace(':', '_')
        elif isinstance(image, str):
            file_tag = image.replace('/', '_').replace(':', '_')
        else:
            raise FailedTest(f'{image} is not a proper image, must be of "str" or "docker.models.images.Image"')
        log_filename = f'{test_name}.log'
        logfile = pathlib.Path(self.location) / 'logs' / file_tag / log_filename
        run_kwargs = {'auto_remove': True,
                      'detach': True,
                      'use_config_proxy': True,
                      'environment': get_system_proxy(),
                      'stdin_open': True,
                      'tty': True,
                      'user': 'root'}
        if kwargs is not None:
            run_kwargs.update(kwargs)

        try:
            if self.container and image not in self.container.image.tags:
                self.container.stop()
                self.container = None
            if self.container and not is_cached:
                self.container.stop()
            if not self.container or not is_cached:
                self.container = self.client.containers.run(image=image, **run_kwargs)
        except APIError as err:
            raise FailedTest(f'Docker daemon API error while starting the container: {err}')

        if not self.container:
            raise FailedTest('Cannot create/start the container')

        try:
            output_total = []
            for command in commands:
                output_total.append(f'    === executing command: {command} ===')
                exit_code, output = self.container.exec_run(cmd=command)
                output_total.append(output.decode('utf-8'))
                if exit_code != 0:
                    log.error(f'- Test {test_name}: command {command} have returned non-zero exit code {exit_code}')
                    log.error(f'Failed command stdout: {output_total[-1]}')
                    logger.switch_to_custom(logfile, str(logfile.parent))
                    for output in output_total:
                        log.error(str(output))
                    logger.switch_to_summary()
                    raise FailedTest(f'Test {test_name}: command {command} '
                                     f'have returned non-zero exit code {exit_code}')
                self.container.reload()
                if self.container.status != 'running':
                    raise FailedTest(f'Test {test_name}: command exit code is 0, but container status != "running" '
                                     'after this command')
            logger.switch_to_custom(logfile, str(logfile.parent))
            for output in output_total:
                log.info(str(output))
            logger.switch_to_summary()

        except APIError as err:
            raise FailedTest(f'Docker daemon API error while executing test {test_name}: {err}')

    def __del__(self):
        """Custom __del__ to manually stop (but not remove) testing container"""
        if self.container:
            self.container.stop()
        super().__del__()
