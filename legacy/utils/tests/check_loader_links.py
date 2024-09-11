# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Utility to check URLs of the release packages embedded inside loader.py"""
import argparse
import os
import sys
import typing
from urllib.request import Request, urlopen
from urllib.error import URLError
from ..loader import INTEL_OPENVINO_VERSION
import logging

logger = logging.getLogger(__name__)


def check_and_print_error(cond, error_msg: str) -> bool:
    """Check condition and print specified error message if it false"""
    if not cond:
        logger.info(error_msg)
    return bool(cond)


def check_release_links(product_version: str) -> typing.Set[bool]:
    """Check some conditions for package URLs of specified release

    Examples:
    * URL must contain the version of the corresponding release with correct distribution
    * Files must be available
    """
    is_minor_release = product_version.count('.') >= 2
    major_version = product_version.rpartition('.')[0] if is_minor_release else product_version
    packages = INTEL_OPENVINO_VERSION[product_version]

    results: typing.Set[bool] = set()
    for image_os in packages:
        for dist in packages[image_os]:
            url = packages[image_os][dist]
            prefix = f'{image_os} {dist}: {url} -'
            # check version and distribution suffixes
            if product_version == '2020.1' and image_os == 'ubuntu18' and dist == 'dev':
                results.add(check_and_print_error(url.count(major_version) == 1, f'{prefix} wrong release'))
                results.add(check_and_print_error(dist in url, f'{prefix} wrong distribution in url'))
            elif major_version >= '2022.2':
                # Staring from 2022.2 there is only one package per OS, without dev/runtime versions
                results.add(check_and_print_error(url.count(major_version) == 2, f'{prefix} wrong * release'))
            elif dist != 'proprietary':
                results.add(check_and_print_error(url.count(major_version) == 2, f'{prefix} wrong release'))
                results.add(check_and_print_error(dist in url, f'{prefix} wrong distribution in url'))
            else:
                results.add(check_and_print_error(url.count(major_version) == 1, f'{prefix} wrong release'))
                results.add(check_and_print_error('runtime' not in url and 'dev' not in url,
                                                  f'{prefix} wrong distribution in url'))

            # check w_ and l_ prefixes
            if 'win' in image_os:
                results.add(check_and_print_error('/w_' in url, f'{prefix} wrong os prefix'))
            else:
                if dist != 'proprietary':
                    results.add(check_and_print_error(image_os in url,
                                                      f'{image_os} {dist}: {url} - wrong image_os'))
                results.add(check_and_print_error('/l_' in url, f'{prefix} wrong os prefix'))

            # check package availability
            req = Request(url, method='HEAD')
            try:
                response = urlopen(req, timeout=4)  # nosec # noqa: S310
                length = int(response.headers['Content-Length'])
                if response.status != 200 or length <= 1000000:
                    results.add(check_and_print_error(False, f'{prefix} network error {response.status}, '
                                                             f'size {length}'))
            except URLError:
                results.add(check_and_print_error(False, f'{prefix} timeout error'))

    logger.info(f'{product_version} - done')
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                     description='Small utility to check embedded URLs of release packages',
                                     add_help=True)
    parser.add_argument(
        '--product_version',
        nargs='?',
        default='',
        help='Product version to check package URLs',
    )
    args = parser.parse_args()
    results_set: typing.Set[bool] = set()
    if args.product_version:
        results_set = results_set.union(check_release_links(args.product_version))
    else:
        for version in INTEL_OPENVINO_VERSION:
            results_set = results_set.union(check_release_links(version))

    if len(results_set) == 1 and next(iter(results_set)):
        logger.info('SUCCESS')
        exit_code = 0
    else:
        logger.info('FAILED')
        exit_code = -1
    sys.exit(exit_code)
