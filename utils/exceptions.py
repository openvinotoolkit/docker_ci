# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Custom exceptions for this framework"""


class FailedStepError(Exception):
    """Generic non-specific exception"""
    pass


class FailedBuildError(Exception):
    """Exception on failed Docker image build"""
    pass


class FailedDeployError(Exception):
    """Exception on failed Docker image push"""
    pass


class FailedTestError(Exception):
    """Exception on failed Docker image test"""
    pass


class LayerNotFoundError(Exception):
    """Exception on missing layer template for Dockerfile render"""
    pass


class InputNotValidError(Exception):
    """Exception on invalid UTF-8 string"""
    pass
