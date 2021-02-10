# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Module handling Dockerfile generating"""
import argparse
import logging
import os
import pathlib
import typing

import jinja2

from utils.exceptions import LayerNotFound
from utils.utilities import get_folder_structure_recursively

log = logging.getLogger('docker_ci')


class DockerFileRender:
    """Handles the creation of dockerfile based on templates and CLI parameters"""

    def __init__(self, os_target: str):
        self.log = jinja2.make_logging_undefined(logger=log)
        self.location = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.os_target = os_target
        self.templates_folders = get_folder_structure_recursively(os.path.join(self.location, 'templates', os_target),
                                                                  ('.*j2',))
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.templates_folders), autoescape=True)

    def get_base_template(self) -> jinja2.environment.Template:
        """Getting base template, above which all additional layers will be applied"""
        return self.env.get_template('base.dockerfile.j2')

    def get_template(self, name: str, kwargs: typing.Dict[str, str]) -> jinja2.environment.Template:
        """Getting needed template file"""
        try:
            return self.env.get_template(f'{name}.dockerfile.j2', globals=kwargs)
        except jinja2.exceptions.TemplateNotFound:
            raise LayerNotFound(f'Layer {name}.dockerfile.j2 was not found. '
                                f'Please add your layer.dockerfile.j2 to '
                                f'<project_root>/templates/<image_os>/layers folder')

    def generate_dockerfile(self, args: argparse.Namespace, kwargs: typing.Dict[str, str]) -> pathlib.Path:
        """Creating of dockerfile based on templates and CLI parameters"""
        settings = []
        if 'win' in args.os:
            if args.msbuild:
                settings.append(args.msbuild)
                settings.append(args.cmake)
            if '2021' in args.year:
                settings.append('vs')
            else:
                settings.append('vs')
                settings.append('icl')
            settings.extend([args.python, args.source, args.install_type, *args.device, args.distribution])
        else:
            pre_device_settings = []
            pre_devices = ['gpu', 'vpu']
            for device in pre_devices:
                if device in args.device:
                    if args.product_version < '2021.3' or device != 'gpu':
                        pre_device_settings.append(f'pre_{device}')
            settings.extend([args.source, args.install_type, *pre_device_settings])

        pre_commands = [self.get_template(arg, kwargs).render() for arg in settings]
        commands = [self.get_template(arg, kwargs).render() for arg in [args.python,
                                                                        args.distribution, *args.device]]
        layers = [self.get_template(arg, kwargs).render() for arg in args.layers]
        save_to_dir = pathlib.Path(self.location) / 'dockerfiles' / args.os
        if not save_to_dir.exists():
            save_to_dir.mkdir()
        save_to = save_to_dir / args.dockerfile_name
        self.get_base_template().stream(pre_commands=pre_commands, commands=commands,
                                        layers=layers, **kwargs).dump(str(save_to))
        log.info('Dockerfile was generated successfully')
        log.info(f'Generated dockerfile location {str(save_to)}')
        return save_to
