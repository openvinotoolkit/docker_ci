# Get Started with DockerHub CI for Intel® Distribution of OpenVINO™ toolkit
This guide provides you with the information that will help you to start using the DockerHub CI framework for OpenVINO™ Toolkit. 
With this guide, you will learn how to:

1. [Generate Dockerfile](#generate-dockerfile)  
2. [Building image](#building-image)  
3. [Deploy image](#deploy-image)  
4. [Test image](#test-image)  
5. [Build, test, deploy an image (All in one)](#all-in-one)  
6. [Run built image](#run-built-image)  

## Generate Dockerfile
To generate Dockerfile with your settings, run the following command in the repository's root:  
```python
python3 docker_openvino.py gen_dockerfile --distribution dev --install_type copy --product_version 2020.4
``` 
You can find generated dockerfile in <root_project>/dockerfiles/<image_os> folder.

Select a product distribution:
```cmd
  -d, --distribution TYPE  Available types: dev, data_dev, runtime, internal_dev, proprietary or 
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

Specify the product package source and install type:
```cmd
  -s, --source {url,local}  Source of the package: external URL or relative <root_project> local path. By default: url.
  --install_type {copy,install}  Installation method for the package. This is "copy" for simple archive and "install" - for exe or archive with installer.
```

Select an image operation system:
```cmd
  -os {ubuntu18,winserver2019} Operation System for docker image. By default: ubuntu18
```

You can customize platform targets and minimize image size:
```cmd
  -d, --device NAME  Target inference hardware: cpu, gpu, vpu, hddl. Default is all.
```

**Prerequisite:** Install the dependencies Microsoft Visual Studio* with C++ 2019, 2017, or 2015 with MSBuild

You can add Visual Studio Build Tools to Windows OS docker image. Previously you need to add offline installer layout in scripts/msbuild2019 folder, 
please follow the official Microsoft [documentation](https://docs.microsoft.com/en-us/visualstudio/install/create-an-offline-installation-of-visual-studio?view=vs-2019).
Or use Build Tools online installer, follow the [documentation](https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container?view=vs-2019) and 
update <repository_root>/templates/winserver2019/msbuild/msbuild2019.dockerfile.j2 dockerfile.
Visual Studio Build Tools are licensed as a supplement your existing Visual Studio license. 
Any images built with these tools should be for your personal use or for use in your organization in accordance with your existing Visual Studio and Windows licenses.
Please don’t share the image with Visual Studio Build Tools on a public Docker hub.
```cmd
  --msbuild {msbuild2019} MSBuild Tools for Windows docker image.
```

You can add your layer and customize image:
```cmd
  -l, --layers NAME  Setup your layer. 
                     Use name of <your_layer>.dockerfile.j2 file located in <project_root>/templates/<image_os>/layers folder. 
                     Layer will be added to the end of product dockerfile. Available layer: model_server (https://github.com/IntelAI/OpenVINO-model-server).
```
You can add your build arguments as well:
```cmd
  --build_arg VAR_NAME=VALUE  Specify build or template arguments for your layer.
```

## Building image

To build images from Dockerfiles, run the following command in the repository's root:  
```python
python3 docker_openvino.py build --package_url <url> --install_type copy
``` 

You can use previously generated dockerfiles from <repository_root>/dockerfiles/<os_image>
```cmd
  -f, --file NAME  Name of the Dockerfile, that will be used to build an image.
```
Specify a tag for image
```cmd
  -t , --tags IMAGE_NAME:TAG  Source image name and optionally a tags in the "IMAGE_NAME:TAG" format. 
                              Default is <os>_<distribution>:<product_version> and latest. You can specify some tags.
```

## Deploy image
**Prerequisite:** previously login to your registry: docker login <registry_url>
To deploy image, run the following command in the repository's root:  
```python
python3 docker_openvino.py deploy --registry docker.io/openvino --tags my_openvino_image:123 --tags my_openvino_image:latest
``` 

**[Mandatory]** Specify a registry and tags for image deploy:
```cmd
   -r, --registry URL:PORT Registry host and optionally a port in the "host:port" format
   -t , --tags IMAGE_NAME:TAG  Source image name and optionally a tags in the "IMAGE_NAME:TAG" format.
```

## Test image
To build and test the image, run the following command in the repository's root:  
```python
python3 docker_openvino.py build_test --package_url <url> --install_type copy
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

**[Mandatory]** Options tag and distribution are mandatory. Image operation system is 'ubuntu18' by default.

## All in one
**Prerequisite:** previously login to your registry: docker login <registry_url>
To gen_dockerfile, build, test and deploy image, run the following command in the repository's root:  
```python
python3 docker_openvino.py all --distribution dev --install_type copy --product_version 2020.2 --registry docker.io/openvino 
``` 
See build and tests logs in <repository_root>/logs/<image_tag> folder and summary.log in <repository_root>/logs

**Note**: if you are building the images on the computer behind the proxy, add needed proxies to the command above 
using the following options:
```
  --http_proxy URL      HTTP proxy settings. By default use system settings.
  --https_proxy URL     HTTPS proxy settings. By default use system settings.
  --ftp_proxy URL       FTP proxy settings. By default use system settings.
  --no_proxy URL        No proxy settings. By default use system settings.
```

There is a number of other parameters that can be passed to `docker_openvino.py`, 
You can see all of them and their descriptions by running:
Available modes: gen_dockerfile, build, build_test, test, deploy, **all**(by default)
```python
python3 docker_openvino.py <mode> --help
```

## Run built image

To start the interactive session, run the following command allows inference on the CPU:

**Linux image:** 
```bash
docker run -it --rm openvino/<image_name>:latest
```
**Windows image** (currently support only CPU target):
```cmd
docker run -it --rm openvino/<image_name>:latest
```
If you want to try some demos then run image with the root privileges (some additional 3-rd party dependencies will be installed):

**Linux image:** 
```bash
docker run -itu root:root --rm openvino/<image_name>:latest /bin/bash -c "apt update && apt install sudo && deployment_tools/demo/demo_security_barrier_camera.sh -d CPU -sample-options -no_show"
```
**Windows image** (currently support only CPU target):
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
To run inference on the HDDL, make sure you've built the image with support for HDDL and setup HDDL drivers on host machine, follow the [configuration guide for HDDL](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux_ivad_vpu.html):
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

---
\* Other names and brands may be claimed as the property of others.