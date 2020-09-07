# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Module handling Docker image building"""
import logging
import pathlib
import typing

from docker.errors import APIError
from docker.models.images import Image

from utils import logger
from utils.docker_api import DockerAPI

log = logging.getLogger('project')


class DockerImageBuilder(DockerAPI):
    """Wrapper for docker.api.client implementing customized build command and logging"""

    def build_docker_image(self,
                           dockerfile: typing.Union[str, pathlib.Path],
                           tag: str,
                           directory: typing.Optional[str] = None,
                           build_args: typing.Optional[typing.Dict[str, str]] = None,
                           logfile: typing.Optional[pathlib.Path] = None) -> typing.Optional[Image]:
        """Build Docker image"""
        if not build_args:
            build_args = {}
        if not directory:
            directory = str(self.location)
        if not logfile:
            logfile = pathlib.Path(directory) / 'logs' / tag / 'build.log'
        dockerfile = str(pathlib.PurePosixPath(str(dockerfile)))

        logfile.parent.mkdir(exist_ok=True, parents=True)

        try:
            log_generator = self.client.api.build(path=directory,
                                                  tag=tag,
                                                  dockerfile=dockerfile,
                                                  rm=True,
                                                  use_config_proxy=True,
                                                  nocache=True,
                                                  pull=True,
                                                  buildargs=build_args,
                                                  decode=True)
            logger.switch_to_custom(logfile, str(logfile.parent))
            log.info(f'build command: docker build {directory} -f {dockerfile} '
                     f'{"".join([f"--build-arg {k}={v} " for k, v in build_args.items()])}')

            for line in log_generator:
                for key, value in line.items():
                    log.info(f'{key} {value}')
                    if key == 'error':
                        logger.switch_to_summary()
                        return None
            logger.switch_to_summary()
            return self.client.images.get(tag)

        except APIError as error:
            log.error(f'Docker server error: {error}')
