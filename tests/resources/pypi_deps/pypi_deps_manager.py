# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Check changes in Python dependencies
"""
import argparse
import difflib
import enum
import json
import logging
import os
import pathlib
import re
import subprocess  # nosec
import sys

import typing
import uuid


@enum.unique
class ExitCode(enum.Enum):
    """Enum that handles the script exitcodes"""
    success = 0
    failed_count = 1
    failed_diff = 2
    unavailable_reqs_config = 3
    missing_req = 4


def get_all_requirements(src: str) -> typing.List[str]:
    """Get list all requirements.txt files in the source folder"""
    requirements = []
    for root, _, file_names in os.walk(src):
        for file_name in file_names:
            if re.match('^.*requirement.*(?:in|txt)$', file_name):
                requirements.append(os.path.join(root, file_name))
    return requirements


def get_pkgs_from_requirement(requirement: typing.Union[str, pathlib.Path]) -> typing.List[str]:
    """Get list of packages in the requirement file"""
    with open(requirement, mode='r') as requirement_file:
        packages = requirement_file.readlines()
    return packages


def get_pot_dependencies(src: str) -> dict:
    """Get POT dependencies from setup.py
            Return: dictionary
            name: path to POT setup.py
            content: list packages"""
    pot_content = {}
    pot_path = pathlib.Path(src) / 'deployment_tools/tools/post_training_optimization_toolkit/setup.py'
    if pot_path.exists():
        pot_path_str = str(pot_path)
        pot_content['name'] = pot_path_str
        cmd_line = ['python3', pot_path_str, 'egg_info']
        process = subprocess.run(cmd_line, cwd=pot_path.parent,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)  # nosec
        pot_requirements = pot_path.parent / 'pot.egg-info/requires.txt'
        if process.returncode == 0:
            pot_content['content'] = get_pkgs_from_requirement(pot_requirements)  # type: ignore
        else:
            pot_content = {}

    return pot_content


def get_image_requirements(src: str) -> dict:
    """Create dictionary to store requirements' data
        Return: dictionary
        main key/value: requirements: list all requirement_filepaths
        other key/value: requirement_filepath: list packages"""
    image_content = {}
    requirements = get_all_requirements(src)
    image_content['requirements'] = requirements
    for requirement in requirements:
        image_content[requirement] = get_pkgs_from_requirement(requirement)
    return image_content


def save_dict_to_json(data: dict, file: str = 'data.json'):
    """Save dictionary to json"""
    with open(file, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)


def load_dict_from_json(file: str) -> dict:
    """Load dictionary to json"""
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def compare_requirements_count(before: typing.List[str], after: typing.List[str], log: str):
    """Compare lists requirements and save in HTML log"""
    with open(pathlib.Path(log) / 'requirements_changes.html', mode='w') as html_log:
        html_log.write(difflib.HtmlDiff().make_file(before, after, 'origin', 'current'))


def compare_packages_settings(before: typing.List[str], after: typing.List[str], context: str, log: str):
    """Compare common packages. Print error in case any changes(need update database)"""
    with open(pathlib.Path(log) / f'pkgs_changes_{uuid.uuid4()}.html', mode='w') as html_log:
        html_log.write(difflib.HtmlDiff().make_file(before, after, 'origin', context))


def main() -> typing.Union[int, ExitCode]:
    """PyPi dependencies manager to get PyPi dependencies and compare with original"""
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                     description='This is PyPi dependencies manager to get PyPi dependencies and '
                                                 'compare with original',
                                     add_help=True)
    parser.add_argument(
        '-i',
        '--image',
        metavar='NAME',
        required=True,
        help='Image name to analyze PyPi dependencies',
    )
    parser.add_argument(
        '-p',
        '--path',
        metavar='NAME',
        default='/opt/intel/openvino',
        help='Path for scanning PyPi dependencies',
    )
    parser.add_argument(
        '-l',
        '--logs',
        metavar='PATH',
        required=False,
        default=str(pathlib.Path(os.path.realpath(__file__)).parent),
        help='Log path folder to store logs',
    )
    parser.add_argument(
        '-j',
        '--image_json',
        metavar='PATH',
        required=False,
        default=None,
        help='Image json file with PyPi dependencies',
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-s',
        '--save',
        action='store_true',
        default=False,
        help="Save the image's PyPi dependencies",
    )
    group.add_argument(
        '-c',
        '--check',
        action='store_true',
        default=False,
        help='Check PyPi dependencies in the image',
    )
    args = parser.parse_args()
    logging.basicConfig(level='INFO')
    log = logging.getLogger(__name__)
    log.info(f'Start analyzing PyPi dependencies for {args.image} image ...')

    image_name = re.search(r'(.*_\d{4}\.\d)', args.image.split('/')[-1].replace(':', '_'))

    if image_name and not args.image_json:
        args.image_json = pathlib.Path(args.logs) / f'{image_name.group(1)}.json'
    elif not image_name and not args.image_json:
        image_name = args.image.split('/')[-1].replace(':', '_')
        args.image_json = pathlib.Path(args.logs) / f'{image_name}.json'

    def add_pot_requirements(path: str, image_content: dict):
        """Search POT requirements from setup.py and add them to image content dict"""
        log.info(f'Search POT dependencies in {path} ...')
        pot_content = get_pot_dependencies(path)
        if pot_content:
            log.info('POT dependencies were found')
            image_content['requirements'].append(pot_content['name'])
            image_content[pot_content['name']] = pot_content['content']
        else:
            log.warning('POT dependencies were not found')
        return image_content

    exit_code = ExitCode.success
    if args.save:
        log.info(f'Save PyPi dependencies in {args.image_json} file')
        image_content = get_image_requirements(args.path)
        if 'runtime' not in args.image:
            add_pot_requirements(args.path, image_content)
        save_dict_to_json(image_content, file=args.image_json)
    else:
        if not pathlib.Path(args.image_json).exists():
            log.error(f'Original data of PyPi dependencies for {args.image_json} is unavailable. '
                      f'Run {os.path.basename(__file__)} with option --save to create it.')
            return ExitCode.unavailable_reqs_config.value

        image_content_original = load_dict_from_json(args.image_json)
        image_content_original_reqs = sorted(image_content_original['requirements'])
        image_content = get_image_requirements(args.path)
        if 'runtime' not in args.image:
            add_pot_requirements(args.path, image_content)
        image_content_reqs = sorted(image_content['requirements'])
        log.info('Compare requirements files by count:')
        if image_content_original_reqs != image_content_reqs:
            log.error('FAILED')
            compare_requirements_count(image_content_original_reqs,
                                       image_content_reqs,
                                       args.logs)
            exit_code = ExitCode.failed_count
        else:
            log.info('PASSED')

        for original_requirement, requirement in zip(image_content_original_reqs, image_content_reqs):
            log.info(f'Find changes in {requirement} file:')
            content_original = image_content_original.get(requirement, None)
            content_image = image_content.get(requirement, None)
            if content_original is None or content_image is None:
                log.error('FAILED: Can not find the requirement file content!')
                exit_code = ExitCode.missing_req
            if content_original != content_image:
                log.error('FAILED')
                compare_packages_settings(image_content_original[original_requirement],
                                          image_content[requirement], requirement, args.logs)
                exit_code = ExitCode.failed_diff
            else:
                log.info('PASSED')
    if exit_code:
        log.info(f'See logs in {args.logs}')

    return exit_code.value


if __name__ == '__main__':
    sys.exit(main())
