# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Module handling auxiliary functions for the framework"""
import os
import pathlib
import re
import typing
import zipfile

import requests

DEFAULT_DATA_CHUNK_SIZE = 64 * 1024  # Chunk size for file downloader (64 KB)


def format_timedelta(timedelta: float) -> str:
    """Custom date & time formatter"""
    days = int(timedelta // (24 * 3600))
    hours = int(timedelta % (24 * 3600) / 3600)
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
        skip = False
        for ignore_pattern in ignore_patterns:
            if re.match(ignore_pattern, item):
                skip = True
                break
        return skip
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
    env = os.environ.copy()
    for name in ('http_proxy', 'https_proxy', 'ftp_proxy', 'no_proxy'):
        if name in env:
            system_proxy[name] = env[name]
            system_proxy[name.upper()] = env[name]
        elif name.upper() in env:
            system_proxy[name] = env[name.upper()]
            system_proxy[name.upper()] = env[name.upper()]
    return system_proxy


def get_converted_system_proxy() -> typing.Dict[str, str]:
    """Getting custom-formatted system proxy"""
    proxy: typing.Dict[str, str] = {}
    env = os.environ.copy()
    for name in ('http_proxy', 'https_proxy', 'ftp_proxy'):
        if name in env:
            proxy[name.split('_')[0]] = env[name]
        elif name.upper() in env:
            proxy[name.split('_')[0]] = env[name.upper()]
    name = 'no_proxy'
    if name in env:
        proxy[name] = env[name]
    elif name.upper() in env:
        proxy[name] = env[name.upper()]
    return proxy


def download_file(url: str, filename: pathlib.Path,
                  proxy: typing.Optional[typing.Dict[str, str]] = None,
                  parents_: bool = False, exist_ok_: bool = True, chunk_size: int = DEFAULT_DATA_CHUNK_SIZE):
    """Custom file downloader that supports careful target save path handling"""
    if not proxy:
        proxy = get_converted_system_proxy()
    filename.parent.mkdir(parents=parents_, exist_ok=exist_ok_)
    with requests.get(url, allow_redirects=True, proxies=proxy, stream=True) as r:
        r.raise_for_status()
        with open(str(filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)


def unzip_file(file_path: str, target_dir: str):
    """Unpack ZIP-archive to specified directory"""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)


def set_windows_system_proxy(system_proxy: typing.Dict[str, str] = None) -> typing.List[str]:
    if not system_proxy:
        system_proxy = get_converted_system_proxy()
    proxy = []
    if 'http' in system_proxy:
        proxy.append(f'set HTTP_PROXY={system_proxy["http"]}')
    if 'https' in system_proxy:
        proxy.append(f'set HTTPS_PROXY={system_proxy["https"]}')
    if 'ftp' in system_proxy:
        proxy.append(f'set FTP_PROXY={system_proxy["ftp"]}')
    if 'no_proxy' in system_proxy:
        proxy.append(f'set NO_PROXY={system_proxy["no_proxy"]}')
    return proxy
