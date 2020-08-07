# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
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


class FailedSave(Exception):
    """Exception on failed Docker image save"""
    pass


class FailedTest(Exception):
    """Exception on failed Docker image test"""
    pass


class LayerNotFound(Exception):
    """Exception on missing layer template for Dockerfile render"""
    pass
