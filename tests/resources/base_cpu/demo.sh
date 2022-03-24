#!/usr/bin/env bash
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

export TBB_DIR=${INTEL_OPENVINO_DIR}/runtime/3rdparty/tbb/cmake

apt update
apt install -y --no-install-recommends make ca-certificates

mkdir -p demo/build
cd demo

curl -O https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/face-detection-adas-0001/FP32/face-detection-adas-0001.bin
curl -O https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/face-detection-adas-0001/FP32/face-detection-adas-0001.xml

echo 'cmake_minimum_required(VERSION 3.4.3)
project(test_ie CXX)
find_package(OpenVINO REQUIRED)
add_executable(${CMAKE_PROJECT_NAME} main.cpp)
target_compile_features(${CMAKE_PROJECT_NAME} PRIVATE cxx_range_for)

target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE openvino::runtime)' > CMakeLists.txt

echo '#include <openvino/openvino.hpp>
#include <iostream>

using namespace ov;

int main(int argc, char** argv){
    Core core;
    std::shared_ptr<Model> model = core.read_model("../face-detection-adas-0001.xml", "../face-detection-adas-0001.bin");
    CompiledModel compiled_model = core.compile_model(model, "CPU");;
    InferRequest infer_request = compiled_model.create_infer_request();
    infer_request.infer();
    std::cout <<"finished" << std::endl;
    return 0;
}' > main.cpp

# Build and run the sample
cd build
cmake ..
cmake --build .
./test_ie
cd ${INTEL_OPENVINO_DIR}