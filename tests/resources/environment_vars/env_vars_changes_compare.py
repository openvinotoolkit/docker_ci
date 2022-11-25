# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Compare environment variables snapshot with expected and detect changes
"""
import argparse
import difflib
import logging
import pathlib
import re
import os
import sys
import typing
import uuid


def normalize_env_variables(variables: typing.Dict[str, str]) -> typing.Dict[str, str]:
    """Cleanup environment variables dict from duplicates in PATH-like variables"""
    output = {}
    for name, value in variables.items():
        if name in ['PATH', 'PYTHONPATH', 'PKG_CONFIG_PATH', 'LD_LIBRARY_PATH', 'LIBRARY_PATH', 'OV_FRONTEND_PATH']:
            paths = set(filter(None, map(str.strip, value.split(':'))))
            output[name] = ':'.join(sorted(paths))
        else:
            output[name] = value
    return output


def extract_changed_environment_variables(vars_before: typing.Dict[str, str],
                                          vars_after: typing.Dict[str, str]) -> typing.Dict[str, str]:
    """Extract current values of environment variables (and handle PATH-like variables as set of values)"""
    return normalize_env_variables(dict(set(vars_after.items()) - set(vars_before.items())))


def load_variables(path: str, env_prefix: bool = False) -> typing.Dict[str, str]:
    """Load environment variables and its values from and env output or a dockerfile-like file"""
    variables = {}
    pattern = re.compile(r'^ENV\s+([A-Za-z_]+)=(.*)$' if env_prefix else r'^([A-Za-z_]+)=(.*)$')
    with open(path) as file:
        for record in filter(None, map(str.strip, file.readlines())):
            match = pattern.match(record)
            if not match:
                return {}
            name = match.group(1)
            value = match.group(2)
            variables[name] = value
    return normalize_env_variables(variables)


def save_env_template(path: pathlib.Path, variables: typing.Dict[str, str]):
    """Save environment variables dict in the file in dockerfile-like format"""
    with open(path, mode='w') as template:
        for name, value in variables.items():
            template.write(f'ENV {name}={value}\n')


def compare_templates(expected_path: pathlib.Path, actual_path: pathlib.Path, image: str, log: str):
    """Compare two template files and save HTML diff"""
    with open(expected_path, mode='r') as expected, \
         open(actual_path, mode='r') as actual, \
         open(pathlib.Path(log) / f'env_{uuid.uuid4()}.html', mode='w') as html_log:
        html_log.write(difflib.HtmlDiff(wrapcolumn=100).make_file(expected.readlines(), actual.readlines(),
                                                                  'origin', image, context=True))


def main() -> int:
    """Compare environment variables snapshot with expected and create HTML report if different"""
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                     description='This is script to extract environment variables changes from '
                                                 'snapshots, compare with expected and create HTML diff report '
                                                 'if different',
                                     add_help=True)
    parser.add_argument(
        '-i',
        '--image',
        metavar='NAME',
        required=True,
        help='Image name',
    )
    parser.add_argument(
        '-e',
        '--expected',
        metavar='PATH',
        required=True,
        help='Path to file with expected environment variable changes from the script',
    )
    parser.add_argument(
        '-b',
        '--before',
        metavar='PATH',
        required=True,
        help='Path to file with environment variables snapshot before script launch',
    )
    parser.add_argument(
        '-a',
        '--after',
        metavar='PATH',
        required=True,
        help='Path to file with environment variables snapshot after script launch',
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

    log.info(f'Parsing inputs...')
    vars_before = load_variables(args.before)
    vars_after = load_variables(args.after)
    vars_created = {name: vars_after[name] for name in set(vars_after.keys()) - set(vars_before.keys())}

    vars_expected = load_variables(args.expected, True)
    vars_expected_updated = {name: vars_after[name] for name in vars_after if name in vars_expected}
    vars_current = {**vars_expected, **vars_created, **vars_expected_updated}

    log.info('Generate updated environment variables template and search for changes:')
    output_path = pathlib.Path(args.logs) / os.path.basename(args.expected)
    save_env_template(output_path, vars_current)
    if vars_expected != vars_current:
        exit_code = 1
        vars_changed_script = extract_changed_environment_variables(vars_before, vars_after)
        vars_changed = extract_changed_environment_variables(vars_expected, vars_current)      
        log.error('FAILED: changes detected')
        log.error(f'    after script launch {vars_changed_script}')
        log.error(f'    with changed {vars_changed}')
        log.error(f'    expected {vars_expected}')
        log.error(f'    current {vars_current}') 

        expected_vars_sorted_path = pathlib.Path(args.logs) / f'sorted_{os.path.basename(args.expected)}'
        save_env_template(expected_vars_sorted_path, vars_expected)
        compare_templates(expected_vars_sorted_path, output_path, args.image, args.logs)
    else:
        exit_code = 0
        log.info('PASSED')
    if vars_created:
        exit_code = 1
        log.error(f'FAILED: new variables are created - {vars_created}')

    if exit_code:
        log.info(f'See logs in {args.logs}')

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
