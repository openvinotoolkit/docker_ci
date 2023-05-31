![Codestyle](https://github.com/openvinotoolkit/docker_ci/workflows/Codestyle%20checks/badge.svg?branch=master)
[![Images build check](https://github.com/openvinotoolkit/docker_ci/actions/workflows/images_build_check.yml/badge.svg?branch=master)](https://github.com/openvinotoolkit/docker_ci/actions/workflows/images_build_check.yml)

# DockerHub CI for [Intel® Distribution of OpenVINO™ toolkit](https://github.com/openvinotoolkit/openvino)

The Framework can generate a Dockerfile, build, test, and deploy an image with the Intel® Distribution of OpenVINO™ toolkit.
You can reuse available Dockerfiles, add your layer and customize the image of OpenVINO™ for your needs.

## Documentation

* [Get Started with OpenVINO™ toolkit images](get-started.md)
* [Available Dockerfiles for OpenVINO™ toolkit](dockerfiles)
* [Generating the dockerfiles and building the images](docs/openvino_docker.md)
* [Working with OpenVINO containers](docs/containers.md)
* [Deployment with GPU accelerators](docs/accelerators.md)
* [Available Tutorials](docs/tutorials)

As [Docker\*](https://docs.docker.com/) is (mostly) just an isolation tool, the OpenVINO toolkit inside the container is the same as the OpenVINO toolkit installed natively on the host machine,
so the [OpenVINO documentation](https://docs.openvino.ai/) is fully applicable to containerized OpenVINO distribution.

## Supported Operating Systems for Docker Base Image:

 - Ubuntu 22.04 LTS
 - Ubuntu 20.04 LTS
 - RedHat UBI 8

## Prebuilt images

Prebuilt images are available on:

- [Docker Hub](https://hub.docker.com/u/openvino)
- [Red Hat* Quay.io](https://quay.io/organization/openvino)
- [Red Hat* Ecosystem Catalog (runtime image)](https://catalog.redhat.com/software/containers/intel/openvino-runtime/606ff4d7ecb5241699188fb3)
- [Red Hat* Ecosystem Catalog (development image)](https://catalog.redhat.com/software/containers/intel/openvino-dev/613a450dc9bc35f21dc4a1f7)
- [Azure* Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/intel_corporation.openvino)

Note: OpenVINO development environment in a docker container is available also in [notebook repository]. It can be deployed in OpenShift RHODS

## Licenses

The DockerHub CI framework for Intel® Distribution of OpenVINO™ toolkit is licensed under [Apache License Version 2.0](./LICENSE).
By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.

**LEGAL NOTICE: Your use of this software and any required dependent software (the "Software Package") is subject to the terms and conditions of the [software license agreements](https://software.intel.com/content/dam/develop/external/us/en/documents/intel-openvino-license-agreements.pdf) for the Software Package, which may also include notices, disclaimers, or license terms for third party or open source software included in or with the Software Package, and your use indicates your acceptance of all such terms.
Please refer to the "third-party-programs.txt" or other similarly-named text file included with the Software Package for additional details.**

Intel is committed to the respect of human rights and avoiding complicity in human rights abuses, a policy reflected in the [Intel Global Human Rights Principles](https://www.intel.com/content/www/us/en/policy/policy-human-rights.html). Accordingly, by accessing the Intel material on this platform you agree that you will not use the material in a product or application that causes or contributes to a violation of an internationally recognized human right.

By downloading and using this container and the included software, you agree to the terms and conditions of the software license agreements located [here](https://software.intel.com/en-us/license/eula-for-intel-software-development-products).
Please, review content inside `<openvino_install_root>/licensing` folder for more details.
As for any pre-built image usage, it is the image user's responsibility to ensure that any use of this image complies with any relevant licenses and potential fees for all software contained within. 
We will have no indemnity or warranty coverage from suppliers.

Components:

- Ubuntu: https://hub.docker.com/_/ubuntu
- Red Hat: https://catalog.redhat.com/software/containers/ubi8/ubi/5c359854d70cc534b3a3784e
- Intel® Distribution of OpenVINO™ toolkit: https://software.intel.com/en-us/license/eula-for-intel-software-development-products

## Security guideline

See [SECURITY](./SECURITY.md) guide for details.

## How to Contribute

See [CONTRIBUTING](./CONTRIBUTING.md) for details. Thank you!

## Support

Please report questions, issues and suggestions using:

* [GitHub* Issues](https://github.com/openvinotoolkit/docker_ci/issues)
* The [`openvino`](https://stackoverflow.com/questions/tagged/openvino) tag on StackOverflow\*
* [Forum](https://software.intel.com/en-us/forums/computer-vision)

---
\* Other names and brands may be claimed as the property of others.
