# -*- coding: utf-8 -*-
# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import cv2

print('OpenCV version:', cv2.getVersionString())
print('OpenVX:', cv2.haveOpenVX())
print('CPUs:', cv2.getNumberOfCPUs())
