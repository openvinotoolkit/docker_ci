#!/usr/bin/env bash
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

export TBB_DIR=${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/tbb/cmake

mkdir -p demo/build
cd demo

curl -O https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/face-detection-adas-0001/FP32/face-detection-adas-0001.bin
curl -O https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/face-detection-adas-0001/FP32/face-detection-adas-0001.xml

echo 'cmake_minimum_required(VERSION 3.4.3)
project(test_ie CXX)
find_package(InferenceEngine REQUIRED)
find_package(ngraph REQUIRED)
add_executable(${CMAKE_PROJECT_NAME} main.cpp)
target_compile_features(${CMAKE_PROJECT_NAME} PRIVATE cxx_range_for)

target_link_libraries(${CMAKE_PROJECT_NAME}
  ${InferenceEngine_LIBRARIES}
  ${NGRAPH_LIBRARIES}
)' > CMakeLists.txt

echo '#include <inference_engine.hpp>
#include <iostream>

using namespace InferenceEngine;

int main(int argc, char** argv){
    Core core;
    CNNNetwork network = core.ReadNetwork("../face-detection-adas-0001.xml", "../face-detection-adas-0001.bin");
    auto executable_network = core.LoadNetwork(network, "CPU");
    auto req = executable_network.CreateInferRequest();
    req.Infer();
    std::cout <<"finished" << std::endl;
    return 0;
}' > main.cpp

# Build and run the sample
cd build
cmake ..
make -j$(nproc)
./test_ie
cd ${INTEL_OPENVINO_DIR}