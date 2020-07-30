# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


class FailedStep(Exception):
    pass


class FailedBuild(Exception):
    pass


class FailedDeploy(Exception):
    pass


class FailedTest(Exception):
    pass


class LayerNotFound(Exception):
    pass
