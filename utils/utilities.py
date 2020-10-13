# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Module handling auxiliary functions for the framework"""
import contextlib
import logging
import os
import pathlib
import re
import tarfile
import typing
import zipfile

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from utils import exceptions

DEFAULT_DATA_CHUNK_SIZE = 64 * 1024  # Chunk size for file downloader (64 KB)
MAX_DEPLOY_RETRIES = 5
SLEEP_BETWEEN_RETRIES = 60 * 10  # Delay between request retries in case of some failures, in seconds

log = logging.getLogger('docker_ci')


def format_timedelta(timedelta: float) -> str:
    """Custom date & time formatter"""
    days = int(timedelta // (24 * 3600))
    hours = int(timedelta % (24 * 3600) / 3600)  # noqa: S001
    minutes = int(timedelta % 3600 / 60)
    seconds = int(timedelta % 60)
    str_date = ''
    if days:
        str_date += f'{days} day' + 's' * (days != 1) + ' '
    if hours or (days and not hours):
        str_date += f'{hours} hour' + 's' * (hours != 1) + ' '
    str_date += f'{minutes} minute' + 's' * (minutes != 1)
    str_date += f' {seconds} second' + 's' * (seconds != 1)
    return str_date


def get_folder_structure_recursively(src: str, ignore: typing.Tuple[str, ...] = ()) -> typing.List[str]:
    """Custom directory traverser that supports regex-based filtering"""
    def should_skip(item):
        for ignore_pattern in ignore_patterns:
            if re.match(ignore_pattern, item):
                return True
        return False

    if not os.path.exists(src):
        return []

    ignore_patterns: typing.Tuple[str, ...] = ('CVS', '.git', '.svn') + ignore

    folder_structure = []

    for root, _, file_names in os.walk(src):
        if not should_skip(root):
            folder_structure.append(root)
        for file_name in file_names:
            if not should_skip(os.path.join(root, file_name)):
                folder_structure.append(os.path.join(root, file_name))
    return folder_structure


def get_system_proxy() -> typing.Dict[str, str]:
    """Getting system proxy"""
    system_proxy: typing.Dict[str, str] = {}
    for proxy_name in ('http_proxy', 'https_proxy', 'ftp_proxy', 'no_proxy'):
        proxy = os.getenv(proxy_name) if os.getenv(proxy_name) else os.getenv(proxy_name.upper())
        if proxy:
            temp_proxy = check_printable_utf8_chars(proxy)
            system_proxy[proxy_name] = temp_proxy
            system_proxy[proxy_name.upper()] = temp_proxy
    return system_proxy


def download_file(url: str, filename: pathlib.Path,
                  proxy: typing.Optional[typing.Dict[str, str]] = None,
                  parents_: bool = False, exist_ok_: bool = True, chunk_size: int = DEFAULT_DATA_CHUNK_SIZE):
    """Custom file downloader that supports careful target save path handling"""
    check_printable_utf8_chars(url)

    if proxy:
        for key in proxy:
            check_printable_utf8_chars(proxy[key])
        log.info(f'Set proxy settings: {proxy}')
    else:
        for key in ('HTTP_PROXY', 'HTTPS_PROXY'):
            check_printable_utf8_chars(str(os.getenv(key)))

    filename.parent.mkdir(parents=parents_, exist_ok=exist_ok_)

    with contextlib.closing(requests.Session()) as http:
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[413, 429, 500, 502, 503, 504, 10054],
        )
        adapter = HTTPAdapter(max_retries=retries)
        http.mount('https://', adapter)
        http.mount('http://', adapter)

        with http.get(url, allow_redirects=True, proxies=proxy, stream=True) as r:
            r.raise_for_status()
            with filename.open(mode='wb') as f:
                for chunk in r.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)


def unzip_file(file_path: str, target_dir: str):
    """Unpack ZIP-archive to specified directory"""
    if file_path.endswith('tgz'):
        with tarfile.open(file_path, 'r') as tar_file:
            tar_file.extractall(target_dir)
    elif file_path.endswith('zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(target_dir)


def check_printable_utf8_chars(string: str) -> str:
    """Validate printable UTF-8 characters for user input"""
    if not isinstance(string, str):
        return string

    string = requests.utils.unquote(string)  # type: ignore
    regex = r"""
    ^(?:
            [\x09\x0A\x0D\x20-\x7E]              # ASCII
            | [\xC2-\xDF][\x80-\xBF]             # non-overlong 2-byte
            |  \xE0[\xA0-\xBF][\x80-\xBF]        # excluding overlongs
            | [\xE1-\xEC\xEE\xEF][\x80-\xBF]{2}  # straight 3-byte
            |  \xED[\x80-\x9F][\x80-\xBF]        # excluding surrogates
            |  \xF0[\x90-\xBF][\x80-\xBF]{2}     # planes 1-3
            | [\xF1-\xF3][\x80-\xBF]{3}          # planes 4-15
            |  \xF4[\x80-\x8F][\x80-\xBF]{2}     # plane 16
        )*$
    """
    if not re.search(regex, string, re.VERBOSE | re.DOTALL):
        raise exceptions.InputNotValid(string)
    return string


def check_internal_local_path(path: str) -> str:
    if not isinstance(path, str):
        return path

    root = str(pathlib.Path(os.path.realpath(__name__)).parent)
    abs_path = str(pathlib.Path(path).absolute())
    # requests.utils.unquote is used twice to decode double encoded strings
    abs_path = requests.utils.unquote(requests.utils.unquote(abs_path))  # type: ignore

    if '..' in abs_path or root not in abs_path:
        raise exceptions.InputNotValid(
            f'Locate file inside <root_project> folder: {path}. Access to the files outside is prohibited.')
    return path
