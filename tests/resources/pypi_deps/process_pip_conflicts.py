# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Read "pip check" output from file and ignore specified errors
"""
import argparse
import fnmatch
import logging
import os
import sys
import typing


def load_error_list(path: str) -> typing.Set[str]:
    """Load list of errors from file (each on a separate line)"""
    with open(path) as file:
        return set(map(str.strip, file.readlines()))


parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='This is pip check errors filter script',
                                 add_help=True)
parser.add_argument(
    '-f',
    '--file',
    metavar='PATH',
    required=True,
    help='Output of "pip check"',
)
parser.add_argument(
    '-w',
    '--whitelist',
    metavar='PATH',
    nargs='+',
    default=[],
    help='Path to file with a list of errors to ignore, each on a separate line',
)

logging.basicConfig(level='INFO')
log = logging.getLogger(__name__)
args = parser.parse_args()
log.info('Start processing pip installed packages check output ...')
current_errors = load_error_list(args.file)

whitelist_errors = set()
for whitelist_path in args.whitelist:
    log.info(f'Loading whitelist file: {whitelist_path}')
    try:
        data = load_error_list(whitelist_path)
        log.info(f'{len(data)} errors will be ignored')
        whitelist_errors.update(data)
    except OSError:
        log.warning(f'Whitelist file {whitelist_path} was not found')

exit_code = 0
for error in current_errors:
    if any((fnmatch.fnmatch(error, pattern) for pattern in whitelist_errors)):
        log.warning(f'Expected pip dependencies error: {error}')
    else:
        exit_code = 1
        log.error(f'New pip dependencies error found: {error}')

if exit_code != 0:
    log.info('FAILED')
else:
    log.info('PASSED')

sys.exit(exit_code)
