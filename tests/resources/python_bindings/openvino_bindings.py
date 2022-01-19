# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import openvino.inference_engine as ie

print('OpenVINO version:', ie.get_version())
print('Available devices: ', ie.IECore().available_devices)
