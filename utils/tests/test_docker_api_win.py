# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from utils.docker_api import DockerAPI
from utils.exceptions import FailedStep

pywintypes = pytest.importorskip('pywintypes')


@pytest.mark.parametrize(('test_exception', 'res_exception'), [
    pytest.param(
        pywintypes.error,
        pywintypes.error,
        id='pywintypes.error',
    ),
    pytest.param(
        pywintypes.error(2, 'WaitNamedPipe'),
        FailedStep,
        id='WaitNamedPipe',
    ),
    pytest.param(
        pywintypes.error(2, 'CreateFile'),
        FailedStep,
        id='CreateFile',
    ),
])
@mock.patch('docker.from_env')
def test_docker_api_init_raises_win(mock_docker, test_exception, res_exception):
    mock_docker.return_value = mock.MagicMock(**{'ping.side_effect': test_exception})
    with pytest.raises(res_exception):
        DockerAPI()
