# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Check GPL/LGPL license for the installed PyPi packages
"""
import argparse
import json
import logging
import os
import sys
import typing


def load_whitelist(path: str) -> typing.Set[str]:
    """Load list of packages to ignore from file (each on a separate line)"""
    with open(path) as file:
        return set(map(str.strip, file.readlines()))


parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='This is GPl/LGPL licenses checker for PyPi packages',
                                 add_help=True)
parser.add_argument(
    '-f',
    '--file',
    metavar='PATH',
    required=True,
    help='JSON file with packages meta',
)
parser.add_argument(
    '-l',
    '--logs',
    metavar='PATH',
    required=False,
    default='pypi_licenses_gpl.json',
    help='Log file in json format',
)
parser.add_argument(
    '-w',
    '--whitelist',
    metavar='PATH',
    nargs='+',
    default=[],
    help='Path to file with a list of package names to ignore, each on a separate line',
)

logging.basicConfig(level='INFO')
log = logging.getLogger(__name__)
args = parser.parse_args()
log.info('Start searching GPl/LGPL licenses in the installed PyPi packages ...')
with open(args.file) as licenses_file:
    pkg_licenses = json.load(licenses_file)

whitelist = set()
for whitelist_path in args.whitelist:
    log.info(f'Loading whitelist file: {whitelist_path}')
    try:
        data = load_whitelist(whitelist_path)
        log.info(f'{len(data)} packages will be ignored')
        whitelist.update(data)
    except OSError:
        log.warning(f'Whitelist file {whitelist_path} was not found')

exit_code = 0
gpl_pkgs = []
for pkg in pkg_licenses:
    if 'GPL' in pkg['License']:
        gpl_pkgs.append(pkg)
        if 'LGPL' not in pkg['License']:
            if pkg['Name'] not in whitelist:
                log.error(f'GPL package was found in PyPi environment: {pkg}')
                exit_code = 1
            else:
                log.warning(f'GPL package was found in PyPi environment and ignored: {pkg}')
log.info(f'Found GPL/LGPL packages: ')
for pkg in gpl_pkgs:
    log.info(pkg)
with open(args.logs, 'w') as gpl_licenses_file:
    json.dump(gpl_pkgs, gpl_licenses_file)
log.info(f'See GPL/LGPL licenses in the json log: {args.logs}')

if exit_code != 0:
    log.info('FAILED')
else:
    log.info('PASSED')

sys.exit(exit_code)
