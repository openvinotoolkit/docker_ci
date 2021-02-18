# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Check GPL/LGPL license for the specified installed apt/yum packages (with the ability to ignore some of them)
"""
import argparse
import logging
import mmap
import os
import sys
import typing

logging.basicConfig(level='INFO')
log = logging.getLogger(__name__)


def load_whitelist(path: str) -> typing.Set[str]:
    """Load list of packages to ignore from file (each on a separate line)"""
    with open(path) as file:
        return set(map(str.strip, file.readlines()))


def filter_gpl_packages_apt(packages: typing.List[dict], whitelist: typing.Set[str]) -> typing.List[str]:
    """Check the selected installed apt packages for the 'GPL' word in their copyright file."""
    found_gpl_packages = []
    for package in packages:
        copyright_file = f'/usr/share/doc/{package["name"]}/copyright'
        if os.path.isfile(copyright_file) and package["name"] not in whitelist:
            with open(copyright_file, 'rb', 0) as file, \
                    mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                if s.find(b'GPL') != -1:
                    log.info(f'Found GPl/LGPL package: {package["name"]}')
                    found_gpl_packages.append(package['name'])
        else:
            log.warning(f'Copyright file for {package["name"]} was not found')
    return found_gpl_packages


def filter_gpl_packages_yum(packages_data: typing.List[dict], whitelist: typing.Set[str]) -> typing.List[str]:
    """Get names of yum packages with GPL license"""
    found_gpl_packages = []
    for package in packages_data:
        if 'GPL' in package['license'] and package['name'] not in whitelist:
            log.info(f'Found GPl/LGPL package: {package["name"]}')
            found_gpl_packages.append(package['name'])
    return found_gpl_packages


def load_packages_table(path: str) -> typing.List[dict]:
    """
    Load packages info from file (each package should be on a separate line with a name, version and
    license (required for yum) columns separated with spaces)
    """
    with open(path) as file:
        packages_info = []
        for line in file.readlines():
            data = list(map(str.strip, filter(None, line.split(' '))))
            packages_info.append({'name': data[0],
                                  'version': data[1],
                                  'license': data[2] if len(data) > 2 else 'unknown'})
        return packages_info


parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='This is GPl/LGPL licenses checker for Linux packages',
                                 add_help=True)

parser.add_argument(
    '-f',
    '--file',
    metavar='PATH',
    required=True,
    help='Path to file with packages info',
)
parser.add_argument(
    '-p',
    '--package_manager',
    choices=['apt', 'yum'],
    required=True,
    help='Path to file with list of packages to ignore',
)
parser.add_argument(
    '-w',
    '--whitelist',
    metavar='PATH',
    nargs='+',
    default=[],
    help='Path to file with list of packages to ignore',
)
parser.add_argument(
    '-l',
    '--logs',
    metavar='PATH',
    default='gpl_packages.txt',
    help='Path to file for saving found GPL packages',
)

args = parser.parse_args()

whitelist = set()
for whitelist_path in args.whitelist:
    log.info(f'Loading whitelist file: {whitelist_path}')
    try:
        data = load_whitelist(whitelist_path)
        log.info(f'{len(data)} packages will be ignored')
        whitelist.update(data)
    except OSError:
        log.warning(f'Whitelist file {whitelist_path} was not found')

log.info('Start searching GPl/LGPL licensed packages ...')
packages_info = load_packages_table(args.file)
if args.package_manager == 'apt':
    gpl_packages = sorted(filter_gpl_packages_apt(packages_info, whitelist))
else:
    gpl_packages = sorted(filter_gpl_packages_yum(packages_info, whitelist))

with open(args.logs, 'w') as gpl_licenses_file:
    gpl_licenses_file.write('\n'.join(gpl_packages))
log.info(f'See GPL/LGPL packages in the log: {args.logs}')

if gpl_packages:
    log.info('FAILED')
else:
    log.info('PASSED')

exit_code = 0 if gpl_packages else 1
sys.exit(exit_code)
