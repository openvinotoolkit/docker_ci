# Dockerfiles with [Intel® Distribution of OpenVINO™ toolkit](https://github.com/openvinotoolkit/openvino)
This repository folder contains Dockerfiles to build an docker image with the Intel® Distribution of OpenVINO™ toolkit.

## Supported Operating Systems for Docker image:
 - `ubuntu18` folder (Ubuntu* 18.04 LTS)
 - `ubuntu20` folder (Ubuntu* 20.04 LTS)
 - `centos7` folder (CentOS* 7.6)
 - `winserver2019` folder (Windows* Server Core base OS LTSC 2019)

## Supported devices and distributions

![OpenVINO Dockerfile Name](../docs/img/dockerfile_name.png)
    
 **Devices:**
 - CPU
 - GPU
 - VPU (NCS2)
 - HDDL (_Prerequisite_: run HDDL daemon on the host machine, follow the [configuration guide for HDDL device](../install_guide_vpu_hddl.md))
 
 **Distributions:**
 - **runtime**: IE core, nGraph, OpenCV, plugins, DL Streamer
 - **dev**: IE core, nGraph, OpenCV, plugins, samples, demo, Python dev tools: Model Optimizer, Post training Optimization tool, Accuracy checker, Model downloader 
 - **data_dev**: runtime + dev + Media SDK, Speech Libraries and End-to-End Speech Demos
 - **base** (only for CPU): IE core, nGraph
 - **proprietary**: data_dev + installer
 
 You can generate Dockerfile with your settings, please follow the [DockerHub CI documentation](../get-started.md).
 * _runtime, dev, data_dev_ distributions based on archive package of OpenVINO product. You can just remove unnecessary parts.
 * _base_ distribution is created by [OpenVINO™ Deployment Manager](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_deployment_manager_tool.html).
 * _proprietary_ distribution based on installer package of OpenVINO product. You can configure installation `COMPONENTS`, follow [Command-Line Silent Instructions](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_linux.html)
## How to build

Base image with CPU only:
```bash
python3 docker_openvino.py build --file "dockerfiles/ubuntu18/openvino_c_base_2020.3.dockerfile" -os ubuntu18 -dist base -p 2020.3.341
```
Or via Docker Engine directly, but you need specify `build_id` argument:
```bash
docker build --build-arg build_id=2020.3.341 -t ubuntu18_base_cpu:2020.3.341 - < dockerfiles/ubuntu18/openvino_c_base_2020.3.dockerfile
```


Dev image:
```bash
python3 docker_openvino.py build --file "dockerfiles/ubuntu18/openvino_cgvh_dev_2021.dockerfile" -os ubuntu18 -dist dev -p 2021.1
```
Or via Docker Engine directly, but you need specify `package_url` argument and OpenCL* version to support GPU:
`GMMLIB`, `IGC_CORE`, `IGC_OPENCL`, `INTEL_OPENCL`, `INTEL_OCLOC`
```bash
docker build --build-arg package_url=https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.1/l_openvino_toolkit_dev_ubuntu18_p_2021.1.110.tgz \
             --build-arg GMMLIB=19.3.2 \
             --build-arg IGC_CORE=1.0.2597 \
             --build-arg IGC_OPENCL=1.0.2597 \
             --build-arg INTEL_OPENCL=19.41.14441 \
             --build-arg INTEL_OCLOC=19.41.14441 \
            -t ubuntu18_dev:2021.1 -f dockerfiles/ubuntu18/openvino_cgvh_dev_2021.dockerfile .
```

## Prebuilt images

Prebuilt images are available on [Docker Hub](https://hub.docker.com/u/openvino)

## Documentation

* [Install Intel® Distribution of OpenVINO™ toolkit for Linux* from a Docker* Image](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_docker_linux.html)
* [Install Intel® Distribution of OpenVINO™ toolkit for Windows* from Docker* Image](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_docker_windows.html)
---
\* Other names and brands may be claimed as the property of others.
