# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Check changes in Linux packages to install
"""
import argparse
import difflib
import logging
import pathlib
import re
import os
import sys
import uuid
import typing


def load_package_list(path: str) -> typing.List[str]:
    """Get package list from text file (each on a separate line)"""
    with open(path) as file:
        return sorted(filter(None, map(str.strip, file.readlines())))


def compare_deps_lists(expected: typing.List[str], actual: typing.List[str], image: str, log: str):
    """Compare two packages lists and save HTML diff"""
    with open(pathlib.Path(log) / f'pkgs_changes_linux_{uuid.uuid4()}.html', mode='w') as html_log:
        html_log.write(difflib.HtmlDiff().make_file(expected, actual, 'origin', image))


def main() -> int:
    """Compare list of packages to install with expected and create HTML report if different"""
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                     description='This is script to compare list of packages to install with expected '
                                                 'and create HTML diff report if different',
                                     add_help=True)
    parser.add_argument(
        '-i',
        '--image',
        metavar='NAME',
        required=True,
        help='Image name to compare dependencies',
    )
    parser.add_argument(
        '-e',
        '--expected',
        metavar='PATH',
        required=True,
        help='Path to file with expected dependencies of image',
    )
    parser.add_argument(
        '-c',
        '--current',
        metavar='PATH',
        required=True,
        help='Path to file with current dependencies of image',
    )
    parser.add_argument(
        '-l',
        '--logs',
        metavar='PATH',
        default=str(pathlib.Path(os.path.realpath(__file__)).parent),
        help='Log path folder to store logs',
    )
    args = parser.parse_args()
    logging.basicConfig(level='INFO')
    log = logging.getLogger(__name__)
    log.info(f'Start comparing dependencies for {args.image} image ...')

    image_name = re.search(r'(.*_\d{4}\.\d)', args.image.split('/')[-1].replace(':', '_'))
    if not image_name:
        log.error('Invalid image name')
        return -1

    packages_expected = load_package_list(args.expected)
    packages_current = load_package_list(args.current)
    log.info('Find changes in package list:')
    exit_code = 0
    if packages_expected != packages_current:
        log.error('FAILED')
        compare_deps_lists(packages_expected, packages_current, image_name.group(1), args.logs)
        exit_code = 1
    else:
        log.info('PASSED')

    if exit_code:
        log.info(f'See logs in {args.logs}')

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
