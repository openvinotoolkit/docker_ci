#!/usr/bin/env bash
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

mkdir -p /tmp/python_bindings

echo "import cv2
print('OpenCV version:', cv2.getVersionString())
print('OpenVX:', cv2.haveOpenVX())
print('CPUs:', cv2.getNumberOfCPUs())
" > /tmp/python_bindings/opencv_bindings.py

echo "import openvino.inference_engine as ie
print('OpenVINO version:', ie.get_version())
print('Available devices: ', ie.IECore().available_devices)
" > /tmp/python_bindings/openvino_bindings.py

echo "import ngraph
print('ngraph has been imported')
" > /tmp/python_bindings/ngraph_bindings.py