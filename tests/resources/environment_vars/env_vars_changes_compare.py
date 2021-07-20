# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Compare environment variables snapshot with expected and detect changes
"""
import argparse
import difflib
import json
import logging
import pathlib
import re
import os
import sys
import typing
import uuid


def load_dict_from_json(file: str) -> dict:
    """Load dictionary to json"""
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def extract_environment_variables(vars_before: typing.Dict[str, str], vars_after: typing.Dict[str, str],
                                  vars_expected: typing.Dict[str, str],
                                  appendable_vars_data: dict, dist: str) -> typing.Dict[str, str]:
    """Extract current values of environment variables (and handle PATH-like variables in a special way)"""
    appendable_vars = appendable_vars_data['appendable_vars']

    vars_current = {name: vars_expected[name] for name in vars_expected if name in vars_after}
    # extract variables created or changed after script launch
    for name, value in sorted(dict(set(vars_after.items()) - set(vars_before.items())).items()):
        if name in appendable_vars and value.endswith(vars_expected[name]) and value != vars_expected[name]:
            base_part = ''
            if name in appendable_vars_data['base_values']:
                base_part += appendable_vars_data['base_values'][name]
            if dist in appendable_vars_data['dist_suffixes'] and name in appendable_vars_data['dist_suffixes'][dist]:
                base_part += appendable_vars_data['dist_suffixes'][dist][name]
            vars_current[name] = value[:-len(vars_expected[name])] + base_part
            if vars_expected[name].endswith(':') and not vars_current[name].endswith(':'):
                vars_current[name] = vars_current[name] + ':'
            elif not vars_expected[name].endswith(':') and vars_current[name].endswith(':'):
                vars_current[name] = vars_current[name][:-1]
        else:
            vars_current[name] = value
    return vars_current


def load_variables(path: str, env_prefix: bool = False) -> typing.Dict[str, str]:
    """Load environment variables and its expected/current values from a dockerfile-like file"""
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
    return variables


def save_env_template(path: pathlib.Path, variables: typing.Dict[str, str]):
    """Save environment variables dict in the file in dockerfile-like format"""
    with open(path, mode='w') as template:
        for name, value in variables.items():
            template.write(f'ENV {name}={value}\n')


def compare_templates(expected_path: pathlib.Path, actual_path: pathlib.Path, image:str, log: str):
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
        '-os',
        '--image_os',
        metavar='NAME',
        required=True,
        help='Image base OS',
    )
    parser.add_argument(
        '-dist',
        '--distribution',
        metavar='NAME',
        required=True,
        help='Image distribution',
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
        '-c',
        '--config',
        metavar='PATH',
        required=True,
        help='Path to config file with custom variable parts (for example, default PATH value from OS)',
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
    appendable_vars_data = load_dict_from_json(args.config)
    vars_before = load_variables(args.before)
    vars_after = load_variables(args.after)
    vars_expected = load_variables(args.expected, True)
    vars_current = extract_environment_variables(vars_before, vars_after, vars_expected,
                                                 appendable_vars_data, args.distribution)

    log.info('Generate updated environment variables template and search for changes:')
    output_path = pathlib.Path(args.logs) / os.path.basename(args.expected)
    save_env_template(output_path, vars_current)
    exit_code = 0
    vars_created = set(vars_after.keys()) - set(vars_before.keys())
    if vars_created:
        exit_code = 1
        log.error(f'FAILED: new variables are created - {vars_created}')
    elif vars_expected != vars_current:
        log.error('FAILED: changes detected')
        exit_code = 1
        compare_templates(args.expected, output_path, args.image, args.logs)
    else:
        log.info('PASSED')

    if exit_code:
        log.info(f'See logs in {args.logs}')

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
