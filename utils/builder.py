# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Module handling Docker image building"""
import logging
import pathlib
import typing

from docker.errors import APIError
from docker.models.images import Image

from utils import logger
from utils.docker_api import DockerAPI

log = logging.getLogger('docker_ci')


class DockerImageBuilder(DockerAPI):
    """Wrapper for docker.api.client implementing customized build command and logging"""

    def build_docker_image(self,
                           dockerfile: typing.Union[str, pathlib.Path],
                           tag: str,
                           directory: typing.Optional[str] = None,
                           build_args: typing.Optional[typing.Dict[str, str]] = None,
                           logfile: typing.Optional[pathlib.Path] = None,
                           no_cache: typing.Optional[bool] = False) -> typing.Optional[Image]:
        """Build Docker image"""
        if not build_args:
            build_args = {}
        if not directory:
            directory = str(self.location)
        if not logfile:
            logfile = pathlib.Path(directory) / 'logs' / tag / 'build.log'

        directory = str(pathlib.Path(directory).as_posix())
        dockerfile = str(pathlib.Path(dockerfile).as_posix())

        logfile.parent.mkdir(exist_ok=True, parents=True)

        try:
            logger.switch_to_custom(logfile, str(logfile.parent))
            log.info(f'build command: docker build {directory} -f {dockerfile} '
                     f'{"".join([f"--build-arg {k}={v} " for k, v in build_args.items()])}')
            log_generator = self.client.api.build(path=directory,
                                                  tag=tag,
                                                  dockerfile=dockerfile,
                                                  rm=True,
                                                  use_config_proxy=True,
                                                  nocache=no_cache,
                                                  pull=True,
                                                  buildargs=build_args,
                                                  decode=True)

            for line in log_generator:
                for key, value in line.items():
                    log.info(f'{key} {value}')
                    if key == 'error':
                        logger.switch_to_summary()
                        log.error(f'{value}')
                        return None
            logger.switch_to_summary()
            return self.client.images.get(tag)

        except APIError as error:
            logger.switch_to_summary()
            log.error(f'Docker server error: {error}')

        return None
