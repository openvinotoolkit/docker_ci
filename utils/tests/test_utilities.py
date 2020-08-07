import zipfile
from unittest import mock

import pytest
import requests

from utils import utilities


@pytest.fixture
def temp_file(tmp_path):
    f = (tmp_path / "file.txt")
    f.write_text("hello")
    return f


@pytest.fixture
def temp_zip(tmp_path, temp_file):
    zip_path = (tmp_path / "temp.zip")
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(temp_file, "file.txt")
    return zip_path


@pytest.mark.parametrize("date, res", [
    pytest.param(
        169310,
        "1 day 23 hours 1 minute 50 seconds",
        id="full date",
    ),
    pytest.param(
        11170.33,
        "3 hours 6 minutes 10 seconds",
        id="0 days",
    ),
    pytest.param(
        3500.74,
        "58 minutes 20 seconds",
        id="0 hours",
    ),
    pytest.param(
        0,
        "0 minutes 0 seconds",
        id="0 seconds",
    ),
])
def test_format_timedelta(date, res):
    assert utilities.format_timedelta(date) == res


class TestDownloadFile:
    def test_correct_url(self, temp_file):
        utilities.download_file(
            url="https://www.google.com/",
            filename=temp_file,
        )
        if not temp_file.exists():
            pytest.fail(f"{temp_file} not found")
        else:
            temp_file.unlink()

    @pytest.mark.parametrize("url, exception", [
        pytest.param(
            "https://www.google.com/test",
            requests.HTTPError,
            id="http_error",
        ),
        pytest.param(
            "",
            requests.exceptions.MissingSchema,
            id="missing_schema",
        ),
        pytest.param(
            "http://",
            requests.exceptions.InvalidURL,
            id="not_host",
        )
    ])
    def test_raises(self, url, exception, temp_file):
        with pytest.raises(exception):
            utilities.download_file(
                url=url,
                filename=temp_file
            )


@pytest.mark.parametrize("mock_data, res", [
    pytest.param(
        {},
        {},
        id="empty proxy list",
    ),
    pytest.param(
        {'http_proxy': 1, 'https_proxy': 2, 'ftp_proxy': 3, 'no_proxy': 4},
        {'http_proxy': 1, 'https_proxy': 2, 'ftp_proxy': 3, 'no_proxy': 4,
         'HTTP_PROXY': 1, 'HTTPS_PROXY': 2, 'FTP_PROXY': 3, 'NO_PROXY': 4},
        id="lowercase proxy list",
    ),
    pytest.param(
        {'HTTP_PROXY': 1, 'HTTPS_PROXY': 2, 'FTP_PROXY': 3, 'NO_PROXY': 4},
        {'http_proxy': 1, 'https_proxy': 2, 'ftp_proxy': 3, 'no_proxy': 4,
         'HTTP_PROXY': 1, 'HTTPS_PROXY': 2, 'FTP_PROXY': 3, 'NO_PROXY': 4},
        id="uppercase proxy list",
    )
])
def test_get_system_proxy(mock_data, res):
    with mock.patch("os.environ.copy") as mock_env:
        mock_env.return_value = mock_data
        assert utilities.get_system_proxy() == res


@pytest.mark.parametrize("mock_data, res", [
    pytest.param(
        {},
        {},
        id="empty proxy list",
    ),
    pytest.param(
        {'http_proxy': 1, 'https_proxy': 2, 'ftp_proxy': 3, 'no_proxy': 4},
        {'http': 1, 'https': 2, 'ftp': 3, 'no_proxy': 4},
        id="lowercase proxy list",
    ),
    pytest.param(
        {'HTTP_PROXY': 1, 'HTTPS_PROXY': 2, 'FTP_PROXY': 3, 'NO_PROXY': 4},
        {'http': 1, 'https': 2, 'ftp': 3, 'no_proxy': 4},
        id="uppercase proxy list",
    )
])
def test_get_converted_system_proxy(mock_data, res):
    with mock.patch("os.environ.copy") as mock_env:
        mock_env.return_value = mock_data
        assert utilities.get_converted_system_proxy() == res


@pytest.mark.parametrize("mock_data, res", [
    pytest.param(
        {},
        [],
        id="empty proxy list",
    ),
    pytest.param(
        {'http': 1, 'https': 2, 'ftp': 3, 'no_proxy': 4},
        ["set HTTP_PROXY=1", "set HTTPS_PROXY=2", "set FTP_PROXY=3", "set NO_PROXY=4"],
        id="not empty proxy list",
    )
])
def test_set_windows_system_proxy(mock_data, res):
    with mock.patch("utils.utilities.get_converted_system_proxy") as mock_get:
        mock_get.return_value = mock_data
        assert utilities.set_windows_system_proxy() == res


class TestUnzipFile:
    @pytest.mark.parametrize("zip_path, exception", [
        pytest.param(
            "",
            FileNotFoundError,
            id="FileNotFoundError",
        ),
        pytest.param(
            "https://www.google.com/test.zip",
            OSError,
            id="OSError",
        ),
    ])
    def test_zip_path_raises(self, zip_path, exception):
        with pytest.raises(exception):
            utilities.unzip_file(zip_path, "")

    def test_not_zip_file(self, temp_file):
        with pytest.raises(zipfile.BadZipfile):
            utilities.unzip_file(temp_file, "")


@pytest.mark.parametrize("mock_data, ignore, res", [
    pytest.param(
        (("root", ["dir1", ".git"], ["file1.txt"]), ("dir1", [".svn", "CVS"], ["hello.doc"]),),
        (".*.txt",),
        ["root", "dir1", "dir1\\hello.doc"],
        id="with ignore",
    ),
    pytest.param(
        (("root", ["dir1", ".git"], ["file1.txt"]), ("dir1", [".svn", "CVS"], ["hello.doc"]),),
        tuple(),
        ["root", "root\\file1.txt", "dir1", "dir1\\hello.doc"],
        id="without ignore",
    ),
])
@ mock.patch("os.walk")
@ mock.patch("os.path.exists")
def test_get_folder_structure_recursively(mock_exists, mock_walk, mock_data, ignore, res):
    mock_exists.return_value = True
    mock_walk.return_value = mock_data
    assert utilities.get_folder_structure_recursively("", ignore) == res
