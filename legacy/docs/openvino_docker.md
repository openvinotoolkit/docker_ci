# Using Docker_CI framework to generate dockerfiles and build the images

DockerHub CI framework based on [Docker SDK for Python](https://github.com/docker/docker-py) - Python library for the Docker Engine API.

## System requirements

*  Python* >=3.8
*  Linux* host
*  Up Docker* engine/service on the host

**Note:** Run DockerHub CI framework on the host machine, nor in a docker container.

## Setup Python environment

1. Create virtual environment `python3 -m venv venv`
2. Activate virtual environment and install requirements: 

    `source venv/bin/activate` - on Linux   
    `pip install -r requirements.txt`
3. Now you can use `docker_openvino.py` to build/test/deploy an image. See detailed instruction below.  

**Note:** Please use Docker CI framework release version corresponding to the version of OpenVINO™ Toolkit.

# How to

This guide provides you with the information that will help you to start using the DockerHub CI framework for OpenVINO™ Toolkit. 
With this guide, you will learn how to:

1. [Generate Dockerfile](#generate-dockerfile)  
2. [Building image](#building-image)  
3. [Deploy image](#deploy-image)  
4. [Test image](#test-image)  
5. [Build, test, deploy an image (All in one)](#all-in-one)  
6. [Troubleshooting](#troubleshooting) 

## Generate Dockerfile
You can use [available Dockerfiles](dockerfiles/README.md) from `<root_project>/dockerfiles/<image_os>` folder or generate Dockerfile with your settings. 
Run the following command in the repository's root:  
```bash
python3 docker_openvino.py gen_dockerfile -os ubuntu20 --distribution dev --product_version 2023.0.0
``` 
You can find generated dockerfile in `<root_project>/dockerfiles/<image_os>` folder. By default, Dockerfile name format is `openvino_<devices>_<distribution>_<product_version>.dockerfile`.

Select a product distribution:
```cmd
  -dist, --distribution TYPE  Available types: dev or runtime. 
                              Using key --file <path_to_dockerfile> and -p <version> are  mandatory to build base distribution image.
                              base dockerfiles are stored in <repository_root>/dockerfiles/<os_image> folder.
```

Select a product version. It will use public released product in docker image:
```cmd
  -p, --product_version  Product version in format: YYYY.U[.BBB], where BBB - build number is optional.

```

Or if you have a product package link, you can specify directly:
You can get OpenVINO distribution packages (runtime, dev) directly from [public storage](https://storage.openvinotoolkit.org/repositories/openvino/packages/).

```cmd
  -u, --package_url URL  Package external or local url, use http://, https://, ftp:// access scheme or relative <root_project> local path
```

**Note:** This is required that OpenVINO package is named in the right way, which is, 
build number (e.g., 2022.1.0.643) have to be part of the URI, 
for example, `openvino_2022.1.0.643.tgz` fits the requirements, while `ov_R3.tgz` is not. 
Otherwise, you should specify `--distribution` and `--product_version` directly.

Specify the product package source:
```cmd
  -s, --source {url,local}  Source of the package: external URL or relative <root_project> local path. By default: url.
 ```

Select an image operation system:
```cmd
  -os {ubuntu22,ubuntu20,rhel8} Operation System for docker image. By default: ubuntu18
```

You can customize platform targets and minimize image size:
```cmd
  -d, --device NAME  Target inference hardware: cpu, gpu. Default is all. 
                     Dockerfile name format has the first letter from device name, 
                     e.g. for CPU, GPU it will be openvino_ch_<distribution>_<product_version>.dockerfile
```

OpenVINO documentation for [supported devices](https://docs.openvino.ai/2023.0/openvino_docs_IE_DG_supported_plugins_Supported_Devices.html).

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
                              You can use "INSTALL_SOURCES=yes" to download source for 3d party LGPL/GPL dependencies.
```

## Building image

To build images from Dockerfiles, run the following command in the repository's root:  
```bash
python3 docker_openvino.py build --package_url <url>
``` 

By default, 'build' mode will generate a dockerfile from templates (see details in the previous section):
```bash
python3 docker_openvino.py build -dist runtime -os ubuntu20 --product_version 2023.0.0
```
but you can specify dockerfile directly:
```cmd
  -f, --file NAME  Name of the Dockerfile, that uses to build an image.
```
Specify a tag for image
```cmd
  -t , --tags IMAGE_NAME:TAG  Source image name and optionally a tags in the "IMAGE_NAME:TAG" format. 
                              Default is <os>_<distribution>:<product_version> and latest. You can specify some tags.
```

```cmd
  --tag_postfix _NAME        Add special postfix to the end of tag image. 
                             Image name will be like this <os>_<distribution>:<product_version><tag_postfix>
```

## Deploy image
**Prerequisite:** previously login to your registry: `docker login <registry_url>`

To deploy image, run the following command in the repository's root:  
```bash
python3 docker_openvino.py deploy --registry docker.io/openvino --tags my_openvino_image:123 --tags my_openvino_image:latest
``` 

**Mandatory:** Specify a registry and tags for image deploy:
```cmd
   -r, --registry URL:PORT Registry host and optionally a port in the "host:port" format
   -t , --tags IMAGE_NAME:TAG  Source image name and optionally a tags in the "IMAGE_NAME:TAG" format.
```

## Test image
To build and test the image, run the following command in the repository's root:  
```bash
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
```bash
python3 docker_openvino.py test --tags <image_name:product_version> -os <image_os> --distribution <type>
``` 

**Mandatory:** Options tag and distribution are mandatory. Image operating system is 'ubuntu18' by default.

Tests can also be run directly using pytest (options image, distribution, image_os are mandatory):
```bash
pytest tests\functional --image <image_name:product_version> --distribution <type> --image_os <image_os> --product_version <product_version>
```
You can filter tests by `-k` (example: `-k "cpu or gpu or vpu"`) or `-m` options (run `pytest --markers` to show available markers).
Warning: pytest doesn't perform validation of the command line arguments what can give less clear error messages than docker_ci

**Note:** You can run tests in parallel by adding `-n auto` option (see [xdist](https://pypi.org/project/pytest-xdist/) documentation for more info).  
Need install pytest-xdist package before: `pip install pytest-xdist`

## All in one
**Prerequisite:** previously login to your registry: `docker login <registry_url>`

To gen_dockerfile, build, test and deploy image, run the following command in the repository's root:  
```bash
python3 docker_openvino.py all --distribution dev --product_version 2023.0.0 --registry docker.io/openvino 
``` 
See build and tests logs in `<repository_root>/logs/<image_tag>` folder and summary.log in `<repository_root>/logs`

**Note:** if you are building the images on the computer behind the proxy, system proxy will be used by default.

There is a number of other parameters that can be passed to `docker_openvino.py`, 
You can see all of them and their descriptions by running:
```bash
python3 docker_openvino.py <mode> --help
```
Available modes: gen_dockerfile, build, build_test, test, deploy, **all**(by default)

## Troubleshooting

If you see a missing `apt` package that needs for OpenVINO product in Linux docker image, please install a missing component directly via `apt install` command and 
create issue on [GitHub* Issues](https://github.com/openvinotoolkit/docker_ci/issues).
We will check a missing package to meet Intel(R) security policy.
Please see [SECURITY](./SECURITY.md) for details to follow security guideline.

If you got a proxy issues, please setup proxy settings for Docker Engine.
DockerHub CI uses a system proxy to generate Dockerfile and build a docker image by default. 


**Check also:**

[Prebuilt images](#prebuilt-images)

[Working with OpenVINO Containers](docs/containers.md)

[Deployment with GPU accelerator](docs/accelerators.md)

[Generating dockerfiles and building the images in Docker_CI tools](docs/openvino_docker.md)


---
\* Other names and brands may be claimed as the property of others.
