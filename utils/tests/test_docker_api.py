import logging
import sys
from unittest import mock

import pytest
import requests

from utils.docker_api import DockerAPI
from utils.exceptions import FailedStep

if sys.platform == 'win32':
    import pywintypes


@pytest.mark.parametrize("test_exception, res_exception", [
    pytest.param(
        requests.exceptions.ConnectionError,
        FailedStep,
        id="ConnectionError",
    ),
    pytest.param(
        pywintypes.error,
        pywintypes.error,
        id="pywintypes.error",
        marks=pytest.mark.skipif(sys.platform != 'win32', reason="pywintypes is win module")
    ),
    pytest.param(
        pywintypes.error(2, 'WaitNamedPipe'),
        FailedStep,
        id="WaitNamedPipe",
        marks=pytest.mark.skipif(sys.platform != 'win32', reason="pywintypes is win module")
    ),
    pytest.param(
        pywintypes.error(2, 'CreateFile'),
        FailedStep,
        id="CreateFile",
        marks=pytest.mark.skipif(sys.platform != 'win32', reason="pywintypes is win module")
    ),
])
@mock.patch("docker.from_env")
def test_docker_api_init_raises(mock_docker, test_exception, res_exception):
    mock_docker.return_value = mock.MagicMock(**{"ping.side_effect": test_exception})
    with pytest.raises(res_exception):
        DockerAPI()


@pytest.mark.parametrize("vers, res", [
    pytest.param(
        {'Version': 1, 'ApiVersion': 2, 'MinAPIVersion': 3, 'Os': 4, 'Arch': 5, 'KernelVersion': 6},
        ('Version: 1', 'ApiVersion: 2', 'MinAPIVersion: 3', 'Os: 4', 'Arch: 5', 'KernelVersion: 6'),
        id="all keys are specified",
    ),
    pytest.param(
        {},
        ('Version: Unknown', 'ApiVersion: Unknown', 'MinAPIVersion: Unknown',
         'Os: Unknown', 'Arch: Unknown', 'KernelVersion: Unknown'),
        id="keys are not specified",
    ),
])
@ mock.patch("docker.from_env")
def test_docker_api_version(mock_docker, caplog, vers, res):
    mock_docker.return_value = mock.MagicMock(**{"version.return_value": vers})
    caplog.set_level(logging.INFO)
    DockerAPI().version()

    for ver in res:
        if ver not in caplog.text:
            pytest.fail("Version doesn't match expectation")
