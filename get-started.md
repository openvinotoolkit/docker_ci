# Get Started with DockerHub CI for Intel® Distribution of OpenVINO™ toolkit

DockerHub CI framework based on [Docker SDK for Python](https://github.com/docker/docker-py) - Python library for the Docker Engine API.

## System requirements

*  Python* >=3.6
*  Windows*/Linux* host
*  Up Docker* engine/service on the host

**Note:** Run DockerHub CI framework on the host machine, nor in a docker container.

## Setup Python environment

1. Create virtual environment `python3 -m venv venv`
2. Activate virtual environment and install requirements: 

    `venv\bin\activate` - on Linux
    
    `venv\Scripts\activate.bat` - on Windows
    
    `pip install -r requirements.txt`
3. Now you can use `docker_openvino.py` to build/test/deploy an image. See detailed instruction below.

# How to

This guide provides you with the information that will help you to start using the DockerHub CI framework for OpenVINO™ Toolkit. 
With this guide, you will learn how to:

1. [Generate Dockerfile](#generate-dockerfile)  
2. [Building image](#building-image)  
3. [Deploy image](#deploy-image)  
4. [Test image](#test-image)  
5. [Build, test, deploy an image (All in one)](#all-in-one)  
6. [Run built image](#run-built-image)  
7. [Troubleshooting](#troubleshooting) 

## Generate Dockerfile
You can use available dockerfiles from `<root_project>/dockerfiles/<image_os>` folder or generate Dockerfile with your settings. 
Run the following command in the repository's root:  
```python
python3 docker_openvino.py gen_dockerfile --distribution dev --product_version 2020.4
``` 
You can find generated dockerfile in `<root_project>/dockerfiles/<image_os>` folder. By default, Dockerfile name format is `openvino_<devices>_<distribution>_<product_version>.dockerfile`.

Select a product distribution:
```cmd
  -dist, --distribution TYPE  Available types: dev, data_dev, runtime, internal_dev, 
                              proprietary (product pkg with an installer) or 
                              base (with CPU only and without installing dependencies). 
                              Using key --file <path_to_dockerfile> is mandatory to build base distribution image.
                              base dockerfiles are stored in <repository_root>/dockerfiles/<os_image> folder.
```

Select a product version. It will use public released product in docker image:
```cmd
  -p, --product_version  Product version in format: YYYY.U[.BBB], where BBB - build number is optional.

```

Or if you have a product package link, you can specify directly:
```cmd
  -u, --package_url URL  Package external or local url, use http://, https://, ftp:// access scheme or relative <root_project> local path
```

**Note:** This is required that OpenVINO package is named in the right way, which is, 
distribution type (runtime, dev) and build number (e.g., 2019.4.420) have to be part of the URI, 
for example, `openvino_dev_2019.3.376.tgz` fits the requirements, while `ov_R3.tgz` is not. 
Otherwise, you should specify `--distribution` and `--product_version` directly.

Specify the product package source:
```cmd
  -s, --source {url,local}  Source of the package: external URL or relative <root_project> local path. By default: url.
 ```

Select an image operation system:
```cmd
  -os {ubuntu18,ubuntu20,centos7,winserver2019} Operation System for docker image. By default: ubuntu18
```

You can customize platform targets and minimize image size:
```cmd
  -d, --device NAME  Target inference hardware: cpu, gpu, vpu, hddl. Default is all. 
                     Dockerfile name format has the first letter from device name, 
                     e.g. for CPU, HDDL it will be openvino_ch_<distribution>_<product_version>.dockerfile
```

**Prerequisite:** Install the dependencies Microsoft Visual Studio* with C++ 2019, 2017, or 2015 with MSBuild

You can add Visual Studio Build Tools to Windows OS docker image. Previously you need to add offline installer layout in scripts/msbuild2019 folder then 
update `<repository_root>/templates/winserver2019/msbuild/msbuild2019.dockerfile.j2` dockerfile, 
please follow the official Microsoft [documentation](https://docs.microsoft.com/en-us/visualstudio/install/create-an-offline-installation-of-visual-studio?view=vs-2019).
Or use Build Tools online installer, follow the [documentation](https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container?view=vs-2019) and 
update `<repository_root>/templates/winserver2019/msbuild/msbuild2019_online.dockerfile.j2` dockerfile.
Visual Studio Build Tools are licensed as a supplement your existing Visual Studio license. 
Any images built with these tools should be for your personal use or for use in your organization in accordance with your existing Visual Studio and Windows licenses.
Please don’t share the image with Visual Studio Build Tools on a public Docker hub.
```cmd
  --msbuild {msbuild2019, msbuild2019_online} MSBuild Tools for Windows docker image.
```

You can add your layer and customize image:
```cmd
  -l, --layers NAME  Setup your layer. 
                     Use name of <your_layer>.dockerfile.j2 file located in <project_root>/templates/<image_os>/layers folder. 
                     Layer will be added to the end of product dockerfile.
```
You can add your build arguments as well:
```cmd
  --build_arg VAR_NAME=VALUE  Specify build or template arguments for your layer.
                              You can use "no_samples=True" to remove OMZ, IE samples and demos from final docker image.
```

## Building image

To build images from Dockerfiles, run the following command in the repository's root:  
```python
python3 docker_openvino.py build --package_url <url>
``` 

By default, 'build' mode will generate a dockerfile, but you can specify dockerfile directly:
```cmd
  -f, --file NAME  Name of the Dockerfile, that uses to build an image.
```
Specify a tag for image
```cmd
  -t , --tags IMAGE_NAME:TAG  Source image name and optionally a tags in the "IMAGE_NAME:TAG" format. 
                              Default is <os>_<distribution>:<product_version> and latest. You can specify some tags.
```

## Deploy image
**Prerequisite:** previously login to your registry: `docker login <registry_url>`

To deploy image, run the following command in the repository's root:  
```python
python3 docker_openvino.py deploy --registry docker.io/openvino --tags my_openvino_image:123 --tags my_openvino_image:latest
``` 

**Mandatory:** Specify a registry and tags for image deploy:
```cmd
   -r, --registry URL:PORT Registry host and optionally a port in the "host:port" format
   -t , --tags IMAGE_NAME:TAG  Source image name and optionally a tags in the "IMAGE_NAME:TAG" format.
```

## Test image
To build and test the image, run the following command in the repository's root:  
```python
python3 docker_openvino.py build_test --package_url <url>
``` 

You can specify a part of the tests to run via option:
```cmd
  -k EXPRESSION         Run tests which match the given substring expression for pytest -k.
```

You can run security and linter tests in the following modes: 'gen_dockerfile', 'build_test', 'test', 'all'. 
The framework installs 3d party docker images or executable files to run security and linter checks:
```cmd
  --sdl_check NAME      Enable SDL check for docker host and image. It installs additional 3d-party docker images or executable files.
                        Available tests: snyk (https://github.com/snyk/snyk), bench_security (https://github.com/docker/docker-bench-security)
  --linter_check NAME   Enable linter check for image and dockerfile. It installs additional 3d-party docker images or executable files.
                        Available tests: hadolint (https://github.com/hadolint/hadolint), dive (https://github.com/wagoodman/dive)
```
To only test your local image:
```python
python3 docker_openvino.py test --tags <image_name:tag> -os <image_os> --distribution <type>
``` 

**Mandatory:** Options tag and distribution are mandatory. Image operation system is 'ubuntu18' by default.

## All in one
**Prerequisite:** previously login to your registry: `docker login <registry_url>`

To gen_dockerfile, build, test and deploy image, run the following command in the repository's root:  
```python
python3 docker_openvino.py all --distribution dev --product_version 2020.2 --registry docker.io/openvino 
``` 
See build and tests logs in `<repository_root>/logs/<image_tag>` folder and summary.log in `<repository_root>/logs`

**Note:** if you are building the images on the computer behind the proxy, system proxy will be used by default.

There is a number of other parameters that can be passed to `docker_openvino.py`, 
You can see all of them and their descriptions by running:
```python
python3 docker_openvino.py <mode> --help
```
Available modes: gen_dockerfile, build, build_test, test, deploy, **all**(by default)
## Run built image

To start the interactive session, run the following command allows inference on the CPU:

**Linux image:** 
```bash
docker run -it --rm openvino/<image_name>:latest
```
**Windows image:** (currently support only CPU target):
```cmd
docker run -it --rm openvino/<image_name>:latest
```

**Linux runtime/data_dev/proprietary images:**

You need to install 3d party dependencies via `<install_root>/install_dependencies/install_openvino_dependencies.sh` in your container to using data processing components:
* DL Streamer*
* GStreamer 
* Speech Libraries and End-to-End Speech Demos

If you want to try some demos then run image with the root privileges (some additional 3-rd party dependencies will be installed):

**Linux image:** 
```bash
docker run -itu root:root --rm openvino/<image_name>:latest /bin/bash -c "apt update && apt install sudo && deployment_tools/demo/demo_security_barrier_camera.sh -d CPU -sample-options -no_show"
```
**Windows image:** (currently support only CPU target):
```cmd
docker run -itu ContainerAdministrator --rm openvino/<image_name>:latest cmd /S /C "cd deployment_tools\demo && demo_security_barrier_camera.bat -d CPU -sample-options -no_show"
```

To enable GPU access, make sure you've built the image with support for GPU and run:
```bash
docker run -itu root:root --rm --device /dev/dri:/dev/dri openvino/<image_name>:latest
```
To run inference on the VPU, make sure you've built the image with support for VPU and run:
```bash
docker run -itu root:root --rm --device-cgroup-rule='c 189:* rmw' -v /dev/bus/usb:/dev/bus/usb openvino/<image_name>:latest
```
To run inference on the HDDL, make sure you've built the image with support for HDDL and setup HDDL driver on host machine, follow the [configuration guide for HDDL device](./install_guide_vpu_hddl.md):
```bash
docker run -itu root:root --rm --device=/dev/ion:/dev/ion -v /var/tmp:/var/tmp openvino/<image_name>:latest
```

And to run inference on all hardware targets supported, make sure you've built the image correctly and run:
```bash
docker run -itu root:root --rm --device=/dev/ion:/dev/ion -v /var/tmp:/var/tmp --device /dev/dri:/dev/dri --device-cgroup-rule='c 189:* rmw' -v /dev/bus/usb:/dev/bus/usb openvino/<image_name>:latest
```

If you want to try some demos then run image with the root privileges (some additional 3-rd party dependencies will be installed):
```bash
docker run -itu root:root --rm --device=/dev/ion:/dev/ion -v /var/tmp:/var/tmp --device /dev/dri:/dev/dri --device-cgroup-rule='c 189:* rmw' -v /dev/bus/usb:/dev/bus/usb openvino/<image_name>:latest
/bin/bash -c "apt update && apt install sudo && deployment_tools/demo/demo_security_barrier_camera.sh -d CPU -sample-options -no_show"
/bin/bash -c "apt update && apt install sudo && deployment_tools/demo/demo_security_barrier_camera.sh -d GPU -sample-options -no_show"
/bin/bash -c "apt update && apt install sudo && deployment_tools/demo/demo_security_barrier_camera.sh -d Myriad -sample-options -no_show"
/bin/bash -c "apt update && apt install sudo && deployment_tools/demo/demo_security_barrier_camera.sh -d HDDL -sample-options -no_show"
```
## Troubleshooting

If you see a missing `apt` package that needs for OpenVINO product in Linux docker image, please install a missing component directly via `apt install` command and 
create issue on [GitHub* Issues](https://github.com/openvinotoolkit/docker_ci/issues).
We will check a missing package to meet Intel(R) security policy.
Please see [SECURITY](./SECURITY.md) for details to follow security guideline.

---
\* Other names and brands may be claimed as the property of others.