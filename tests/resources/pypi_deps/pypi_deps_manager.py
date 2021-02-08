# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Check changes in Python dependencies
"""
import argparse
import difflib
import json
import logging
import os
import pathlib
import re
import sys

import typing
import uuid


def get_all_requirements(src: str) -> typing.List[str]:
    """Get list all requirements.txt files in the source folder"""
    requirements = []
    for root, _, file_names in os.walk(src):
        for file_name in file_names:
            if re.match('^.*requirement.*(?:in|txt)$', file_name):
                requirements.append(os.path.join(root, file_name))
    return requirements


def get_pkgs_from_requirement(requirement: str) -> typing.List[str]:
    """Get list of packages in the requirement file"""
    with open(requirement, mode='r') as requirement_file:
        packages = requirement_file.readlines()
    return packages


def get_image_requirements(src) -> dict:
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


def main() -> int:
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

    exit_code = 0
    if args.save:
        log.info(f'Save PyPi dependencies in {args.image_json} file')
        image_content = get_image_requirements(args.path)
        save_dict_to_json(image_content, file=args.image_json)
    else:
        if not pathlib.Path(args.image_json).exists():
            log.error(f'Original data of PyPi dependencies for {args.image_json} is unavailable. '
                      f'Run {os.path.basename(__file__)} with option --save to create it.')
            return 3

        image_content_original = load_dict_from_json(args.image_json)
        image_content_original_reqs = sorted(image_content_original['requirements'])
        image_content = get_image_requirements(args.path)
        image_content_reqs = sorted(image_content['requirements'])
        log.info('Compare requirements files by count:')
        if image_content_original_reqs != image_content_reqs:
            log.error('FAILED')
            compare_requirements_count(image_content_original_reqs,
                                       image_content_reqs,
                                       args.logs)
            exit_code = 1
        else:
            log.info('PASSED')

        for original_requirement, requirement in zip(image_content_original_reqs, image_content_reqs):
            log.info(f'Find changes in {requirement} file:')
            if image_content_original[original_requirement] != image_content[requirement]:
                log.error('FAILED')
                compare_packages_settings(image_content_original[original_requirement],
                                          image_content[requirement], requirement, args.logs)
                exit_code = 2
            else:
                log.info('PASSED')
    if exit_code:
        log.info(f'See logs in {args.logs}')

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
