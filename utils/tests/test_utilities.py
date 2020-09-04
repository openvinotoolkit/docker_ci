# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pathlib
import zipfile
from unittest import mock

import pytest
import requests

from utils import exceptions, utilities


@pytest.fixture()
def temp_file(tmp_path):
    f = (tmp_path / 'file.txt')
    f.write_text('hello')
    return f


@pytest.fixture()
def temp_zip(tmp_path, temp_file):
    zip_path = (tmp_path / 'temp.zip')
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(temp_file, 'file.txt')
    return zip_path


@pytest.mark.parametrize('date, res', [
    pytest.param(
        169310,
        '1 day 23 hours 1 minute 50 seconds',
        id='full date',
    ),
    pytest.param(
        11170.33,
        '3 hours 6 minutes 10 seconds',
        id='0 days',
    ),
    pytest.param(
        3500.74,
        '58 minutes 20 seconds',
        id='0 hours',
    ),
    pytest.param(
        0,
        '0 minutes 0 seconds',
        id='0 seconds',
    ),
])
def test_format_timedelta(date, res):
    assert utilities.format_timedelta(date) == res  # noqa: S101  # nosec


class TestDownloadFile:
    def test_valid_url(self, temp_file):
        utilities.download_file(
            url='https://www.google.com/',
            filename=temp_file,
        )
        if not temp_file.exists():
            pytest.fail(f'{temp_file} not found')
        else:
            temp_file.unlink()

    @pytest.mark.parametrize('url, exception', [
        pytest.param(
            'https://www.google.com/test',
            requests.HTTPError,
            id='http_error',
        ),
        pytest.param(
            '',
            requests.exceptions.MissingSchema,
            id='missing_schema',
        ),
        pytest.param(
            'http://',
            requests.exceptions.InvalidURL,
            id='not_host',
        ),
        pytest.param(
            '\xED\xBF\xBF',
            exceptions.InputNotValid,
            id='url string is not utf-8',
        ),
        pytest.param(
            'https:\00\0n',
            exceptions.InputNotValid,
            id='url string with null char',
        ),
    ])
    def test_invalid_url(self, url, exception, temp_file):
        with pytest.raises(exception):
            utilities.download_file(
                url=url,
                filename=temp_file,
            )

    @mock.patch('requests.Session')
    def test_valid_proxy(self, mock_session, temp_file):
        mock_session.return_value = mock.MagicMock(**{'get.side_effect': Exception('Proxy check')})
        try:
            utilities.download_file(
                url='https://www.google.com/test',
                proxy={'https': 'https://www.google.com/test'},
                filename=temp_file,
            )
        except Exception as e:
            assert str(e) == 'Proxy check'  # noqa: S101  # nosec

    @pytest.mark.parametrize('proxy, exception', [
        pytest.param(
            {'http': '\00\0n'},
            exceptions.InputNotValid,
            id='proxy string with null char',
        ),
        pytest.param(
            {'https': '\xED\xBF\xBF'},
            exceptions.InputNotValid,
            id='proxy string is not utf-8',
        ),
    ])
    def test_invalid_proxy(self, proxy, exception, temp_file):
        with pytest.raises(exception):
            utilities.download_file(
                url='https://www.google.com',
                proxy=proxy,
                filename=temp_file,
            )


@pytest.mark.parametrize('mock_data, res', [
    pytest.param(
        {},
        {},
        id='empty proxy list',
    ),
    pytest.param(
        {'http_proxy': '1', 'https_proxy': '2', 'ftp_proxy': '3', 'no_proxy': '4'},
        {'http_proxy': '1', 'https_proxy': '2', 'ftp_proxy': '3', 'no_proxy': '4',
         'HTTP_PROXY': '1', 'HTTPS_PROXY': '2', 'FTP_PROXY': '3', 'NO_PROXY': '4'},
        id='lowercase proxy list',
    ),
    pytest.param(
        {'HTTP_PROXY': '1', 'HTTPS_PROXY': '2', 'FTP_PROXY': '3', 'NO_PROXY': '4'},
        {'http_proxy': '1', 'https_proxy': '2', 'ftp_proxy': '3', 'no_proxy': '4',
         'HTTP_PROXY': '1', 'HTTPS_PROXY': '2', 'FTP_PROXY': '3', 'NO_PROXY': '4'},
        id='uppercase proxy list',
    ),
])
def test_get_system_proxy(mock_data, res):
    with mock.patch('os.environ.copy') as mock_env:
        mock_env.return_value = mock_data
        assert utilities.get_system_proxy() == res  # noqa: S101  # nosec


class TestUnzipFile:
    @pytest.mark.parametrize('zip_path, exception', [
        pytest.param(
            '',
            FileNotFoundError,
            id='FileNotFoundError',
        ),
        pytest.param(
            'https://www.google.com/test.zip',
            OSError,
            id='OSError',
        ),
    ])
    def test_zip_path_raises(self, zip_path, exception):
        with pytest.raises(exception):
            utilities.unzip_file(zip_path, '')

    def test_not_zip_file(self, temp_file):
        with pytest.raises(zipfile.BadZipfile):
            utilities.unzip_file(temp_file, '')


@pytest.mark.parametrize('mock_data, ignore, res', [
    pytest.param(
        (('root', ['dir1', '.git'], ['file1.txt']), ('dir1', ['.svn', 'CVS'], ['hello.doc'])),
        ('.*.txt',),
        ['root', 'dir1', 'dir1/hello.doc'],
        id='with ignore',
    ),
    pytest.param(
        (('root', ['dir1', '.git'], ['file1.txt']), ('dir1', ['.svn', 'CVS'], ['hello.doc'])),
        (),
        ['root', 'root/file1.txt', 'dir1', 'dir1/hello.doc'],
        id='without ignore',
    ),
])
@ mock.patch('os.walk')
@ mock.patch('os.path.exists')
def test_get_folder_structure_recursively(mock_exists, mock_walk, mock_data, ignore, res):
    mock_exists.return_value = True
    mock_walk.return_value = mock_data
    out = list(map(lambda path: pathlib.Path(path).as_posix(), utilities.get_folder_structure_recursively('', ignore)))
    assert out == res  # noqa: S101  # nosec


class TestCheckPrintableUTF8Chars:
    @pytest.mark.parametrize('string', [
        pytest.param(
            'https://www.google.com',
            id='URL',
        ),
        pytest.param(
            'C:\\User\\00\\Desktop',
            id='WindowsPath',
        ),
        pytest.param(
            '/usr/tmp/app.py',
            id='LinuxPath',
        ),
        pytest.param(
            '2af2t3g3gk65l',
            id='Token',
        ),
        pytest.param(
            None,
            id='None',
        ),
    ])
    def test_valid_input(self, string):
        assert utilities.check_printable_utf8_chars(string) == string  # noqa: S101  # nosec

    @pytest.mark.parametrize('string', [
        pytest.param(
            'https://www.google.com/1.py%002.zip',
            id='URL',
        ),
        pytest.param(
            'C:\\User\00\\Desktop',
            id='WindowsPath',
        ),
        pytest.param(
            '../../web.xml\0abcdef.pdf',
            id='LinuxPath',
        ),
        pytest.param(
            '2af2%00t3g3gk65l',
            id='Token',
        ),
    ])
    def test_invalid_input(self, string):
        with pytest.raises(exceptions.InputNotValid):
            utilities.check_printable_utf8_chars(string)


class TestCheckInternalLocalPath:
    @pytest.mark.parametrize('path', [
        pytest.param(
            'test.zip',
            id='file',
        ),
        pytest.param(
            'hello/test.zip',
            id='folder/file',
        ),
        pytest.param(
            None,
            id='None',
        ),

    ])
    def test_valid_relative_path(self, path):
        assert utilities.check_internal_local_path(path) == path  # noqa: S101  # nosec

    @pytest.mark.parametrize('path', [
        pytest.param(
            '../test.zip',
            id='../',
        ),
        pytest.param(
            '..../test.zip',
            id='..../',
        ),
        pytest.param(
            '%2e%2e/MYFILE.TXT',
            id='encoded 1',
        ),
        pytest.param(
            '%2e%2e%2fMYFILE.TXT',
            id='encoded 2',
        ),
        pytest.param(
            '%252E%252E%252FMYFILE.TXT',
            id='double encoded',
        ),
        pytest.param(
            'MYFILE..TXT',
            id='..txt',
        ),
    ])
    def test_invalid_relative_path(self, path):
        with pytest.raises(exceptions.InputNotValid):
            utilities.check_internal_local_path(path)

    @pytest.mark.parametrize('root, path', [
        pytest.param(
            'c:/dockerhub',
            'c:/dockerhub/readme.txt',
            id='file',
        ),
        pytest.param(
            'c:/dockerhub',
            'c:/dockerhub/utils/get_started.txt',
            id='folder/file',
        ),
    ])
    @mock.patch('pathlib.Path')
    def test_valid_abs_path(self, mock_path, root, path):
        temp_mock = mock.MagicMock(**{'absolute.return_value': path})
        temp_mock.parent = root
        mock_path.return_value = temp_mock
        assert utilities.check_internal_local_path(path) == path  # noqa: S101  # nosec

    @pytest.mark.parametrize('root, path', [
        pytest.param(
            'c:/dockerhub',
            'c:/dockerhub/../secret.txt',
            id='../',
        ),
        pytest.param(
            'c:/dockerhub',
            'c:/dockerhub/..../secret.txt',
            id='..../',
        ),
        pytest.param(
            'c:/dockerhub',
            'c:/desktop/secret.txt',
            id='other dir',
        ),
        pytest.param(
            '/usr/tmp/dockerhub',
            '/',
            id='root dir',
        ),
        pytest.param(
            '/usr/tmp/dockerhub',
            '/usr/tmp/dockerhub/%2e%2e/secret.txt',
            id='encoded 1',
        ),
        pytest.param(
            '/usr/tmp/dockerhub',
            '/usr/tmp/dockerhub/%2e%2e%2fsecret.txt',
            id='encoded 2',
        ),
        pytest.param(
            '/usr/tmp/dockerhub',
            '/usr/tmp/dockerhub/%252E%252E%252Fsecret.txt',
            id='double encoded',
        ),
        pytest.param(
            '/usr/tmp/dockerhub',
            '/usr/tmp/dockerhub/readme..txt',
            id='..txt',
        ),
    ])
    @mock.patch('pathlib.Path')
    def test_invalid_abs_path(self, mock_path, root, path):
        temp_mock = mock.MagicMock(**{'absolute.return_value': path})
        temp_mock.parent = root
        mock_path.return_value = temp_mock
        with pytest.raises(exceptions.InputNotValid):
            utilities.check_internal_local_path(path)
