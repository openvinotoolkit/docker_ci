# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Custom exceptions for this framework"""


class FailedStep(Exception):
    """Generic non-specific exception"""
    pass


class FailedBuild(Exception):
    """Exception on failed Docker image build"""
    pass


class FailedDeploy(Exception):
    """Exception on failed Docker image push"""
    pass


class FailedTest(Exception):
    """Exception on failed Docker image test"""
    pass


class LayerNotFound(Exception):
    """Exception on missing layer template for Dockerfile render"""
    pass


class InputNotValid(Exception):
    """Exception on invalid UTF-8 string"""
    pass
