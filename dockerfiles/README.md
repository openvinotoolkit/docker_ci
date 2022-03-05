# Dockerfiles with [Intel® Distribution of OpenVINO™ toolkit](https://github.com/openvinotoolkit/openvino)

This repository folder contains Dockerfiles to build an docker image with the Intel® Distribution of OpenVINO™ toolkit.
You can use Docker CI framework to build an image, please follow [Get Started with DockerHub CI for Intel® Distribution of OpenVINO™ toolkit](../get-started.md).

1. [Supported Operating Systems for Docker image](#supported-operating-systems-for-docker-image)  
2. [Supported devices and distributions](#supported-devices-and-distributions)  
3. [Where to get OpenVINO package](#where-to-get-openvino-package)
4. [How to build](#how-to-build)  
5. [Prebuilt images](#prebuilt-images)  
6. [How to run a container](#how-to-run-a-container)  

## Supported Operating Systems for Docker image

 - `ubuntu18` folder (Ubuntu* 18.04 LTS)
 - `ubuntu20` folder (Ubuntu* 20.04 LTS)
 - `rhel8` folder (RHEL* 8)
 - `winserver2019` folder (Windows* Server Core base OS LTSC 2019)
 - `windows20h2` folder (Windows* OS 20H2)

*Note*: `dl-workbench` folder contains Dockerfiles for OpenVINO™ Deep Learning Workbench.

## Supported devices and distributions

![OpenVINO Dockerfile Name](../docs/img/dockerfile_name.png)

 **Devices:**
 - CPU
 - GPU
 - VPU (NCS2)
 - HDDL (VPU HDDL) (_Prerequisite_: run HDDL daemon on the host machine, follow the [configuration guide for HDDL device](../install_guide_vpu_hddl.md))

 OpenVINO documentation for [supported devices](https://docs.openvinotoolkit.org/latest/openvino_docs_IE_DG_supported_plugins_Supported_Devices.html).

 **Distributions:**

 - **runtime**: IE core, nGraph, plugins
 - **dev**: IE core, nGraph, plugins, samples, Python dev tools: Model Optimizer, Post training Optimization tool, Accuracy checker, Open Model Zoo tools (downloader, converter)
 - **base** (only for CPU): IE core, nGraph

You can generate Dockerfile with your settings, please follow the [DockerHub CI documentation](../get-started.md).
 * _runtime_ and _dev_ distributions are based on archive package of OpenVINO product. You can just remove unnecessary parts.
 * _base_ distribution is created by [OpenVINO™ Deployment Manager](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_deployment_manager_tool.html).

## Where to get OpenVINO package

You can get OpenVINO distribution packages (runtime, dev) directly from [public storage](https://storage.openvinotoolkit.org/repositories/openvino/packages/).
For example: 
* take runtime `l_openvino_toolkit_runtime_ubuntu18_p_2021.2.185.tgz` package and specify `-dist runtime` option for Docker CI `docker_openvino.py` or take a Dockerfile with `runtime` suffix.

## How to build

**Note:** Please use Docker CI framework release version corresponding to the version of OpenVINO™ Toolkit that you need to build.

* Base image with CPU only:

You can use Docker CI framework to build an image, please follow [Get Started with DockerHub CI for Intel® Distribution of OpenVINO™ toolkit](../get-started.md).

```bash
python3 docker_openvino.py build --file "dockerfiles/ubuntu18/openvino_c_base_2020.3.dockerfile" -os ubuntu18 -dist base -p 2020.3.341
```
Or via Docker Engine directly, but you need specify `BUILD_ID` argument:
```bash
docker build --build-arg BUILD_ID=2020.3.341 -t ubuntu18_base_cpu:2020.3.341 - < dockerfiles/ubuntu18/openvino_c_base_2020.3.dockerfile
```
----------------

* Dev/runtime image:

You can use Docker CI framework to build an image, please follow [Get Started with DockerHub CI for Intel® Distribution of OpenVINO™ toolkit](../get-started.md).

```bash
python3 docker_openvino.py build --file "dockerfiles/ubuntu18/openvino_cgvh_dev_2021.dockerfile" -os ubuntu18 -dist dev -p 2021.1
```
For runtime distribution, please set appropriate `-dist` and `--file` options.

Or via Docker Engine directly, but you need specify `package_url` argument (see [Where to get OpenVINO package section](#where-to-get-openvino-package)):
```bash
docker build --build-arg package_url=https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/l_openvino_toolkit_dev_ubuntu18_p_2021.4.582.tgz \
             -t ubuntu18_dev:2021.4 -f dockerfiles/ubuntu18/openvino_cgvh_dev_2021.4.dockerfile .
```
----------------

* Custom image with CPU, iGPU, VPU support  
You can use Dockerfiles from the `build_custom` folders to build a custom version of OpenVINO™ from source code for development. To learn more, follow:
  * [Build custom Intel® Distribution of OpenVINO™ toolkit Docker image on Ubuntu 18](ubuntu18/build_custom/README.md)
  * [Build custom Intel® Distribution of OpenVINO™ toolkit Docker image on Ubuntu 20](ubuntu20/build_custom/README.md)

## Prebuilt images

Prebuilt images are available on: 
- [Docker Hub](https://hub.docker.com/u/openvino)
- [Red Hat* Quay.io](https://quay.io/organization/openvino)
- [Red Hat* Ecosystem Catalog](https://catalog.redhat.com/software/containers/intel/openvino-runtime/606ff4d7ecb5241699188fb3)
- [Azure* Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/intel_corporation.openvino)


## How to run a container

Please follow [Run a container](../get-started.md#run-a-container) section in DockerHub CI getting started guide.

## Documentation

* [Install Intel® Distribution of OpenVINO™ toolkit for Linux* from a Docker* Image](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_docker_linux.html)
* [Install Intel® Distribution of OpenVINO™ toolkit for Windows* from Docker* Image](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_docker_windows.html)
* [Official Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

---
\* Other names and brands may be claimed as the property of others.
