# Build Intel® Distribution of OpenVINO™ toolkit Docker image using Red Hat® OpenShift® Container Platform 

This repository folder contains Dockerfile to build an image with the Intel® Distribution of OpenVINO™ toolkit using Red Hat® OpenShift® Container Platform.

## Prebuilt images

Prebuilt images are available on [Red Hat* Quay.io](https://quay.io/organization/openvino) and [Red Hat* Ecosystem Catalog](https://catalog.redhat.com/software/containers/intel/openvino-runtime/606ff4d7ecb5241699188fb3) Registries.

## Prerequisites

You need Red Hat Enterprise Linux 8 host with installed [Openshift Container Platform 4](https://docs.openshift.com/container-platform/4.6/welcome/index.html).  
>**Note**: 
> You can use [Red Hat® CodeReady Containers](https://cloud.redhat.com/openshift/create/local) to create a minimal single node cluster for development and testing on a local PC.
> Read more [here](https://access.redhat.com/documentation/en-us/red_hat_codeready_containers/1.23/).

## How to build

### Configure host
1. Create a new folder and place the following files in it:
    * Dockerfile
    * OpenVINO package (please read [Where to get OpenVINO package](../../README.md#where-to-get-openvino-package) section in the dockerfiles readme.)
    * `rhsm.conf` (you can take it from `/etc/rhsm/` folder)
    * `redhat-uep.pem` (you can take it from `/etc/rhsm/ca` folder)
    * RedHat subscription certificate of your node (you can download it from Red Hat Customer Portal)


2. Create a build secret with your Red Hat® subscription certificate:
```shell
oc create secret generic entitlement --from-file=entitlement.pem=<your-certificate>.pem --from-file=entitlement-key.pem=<your-certificate>.pem
```
3. Create build configmaps with Red Hat® subscription manager configuration:
```shell
oc create configmap rhsm-conf --from-file rhsm.conf
oc create configmap rhsm-ca --from-file redhat-uep.pem
```
### Create build configuration
```shell
 cat openvino_cg_openshift_runtime_2021.3.dockerfile | oc new-build --name <build-name> --dockerfile='-' --build-secret entitlement \
                                                          --build-config-map rhsm-conf:rhsm-conf --build-config-map rhsm-ca:rhsm-ca \
                                                          --build-arg INTEL_OPENCL=<intel-opencl-version> \ 
                                                          --build-arg package_url=<openvino-tgz-package-name>
```
You can use `--build-arg` option to override the `INTEL_OPENCL` variable to specify the version of Intel® Graphics Compute Runtime 
for OpenCL™ Driver on Linux. It is equal to "19.41.14441" by default.

>**Note**:  
> Read specified RedHat documentation pages for more info:
> * [Using Red Hat subscriptions in builds](https://docs.openshift.com/container-platform/4.6/builds/running-entitled-builds.html)
> * [How to use entitled image builds to build DriverContainers with UBI on OpenShift](https://www.openshift.com/blog/how-to-use-entitled-image-builds-to-build-drivercontainers-with-ubi-on-openshift)
> * [How to use entitled image builds on Red Hat OpenShift Container Platform 4.x cluster ?](https://access.redhat.com/solutions/4908771)

### Start build
```shell
oc start-build <build-name> --from-file <openvino-tgz-package-name> --no-cache=true --follow 
```
---
\* Other names and brands may be claimed as the property of others.
