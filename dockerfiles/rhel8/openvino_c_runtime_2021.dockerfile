# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM registry.access.redhat.com/ubi8/ubi:8.2 AS base

# hadolint ignore=DL3002
USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# hadolint ignore=DL3031, DL3033
RUN yum update -y && yum install -y curl ca-certificates && \
    yum clean all && rm -rf /var/cache/yum


# get product from URL
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}

# install product by copying archive content
ARG TEMP_DIR=/tmp/openvino_installer
ENV INTEL_OPENVINO_DIR /opt/intel/openvino

RUN tar -xzf "${TEMP_DIR}"/*.tgz && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d+')" && \
    OV_YEAR="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino_"$OV_YEAR" && \
    rm -rf ${INTEL_OPENVINO_DIR}/deployment_tools/tools/workbench && rm -rf ${TEMP_DIR}


# -----------------
FROM registry.access.redhat.com/ubi8/ubi:8.2 AS ov_base

LABEL Description="This is the runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on RHEL 8.2"
LABEL Vendor="Intel Corporation"

USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Creating user openvino and adding it to group "users"
RUN useradd -ms /bin/bash -G users openvino && \
    chown openvino -R /home/openvino

RUN mkdir /opt/intel

ENV INTEL_OPENVINO_DIR /opt/intel/openvino

COPY --from=base /opt/intel /opt/intel

ARG LGPL_DEPS="gcc-c++ \
               gtk3"

# hadolint ignore=DL3031, DL3033
RUN yum -y update && yum install -y yum-utils ${LGPL_DEPS} && \
    yum clean all && rm -rf /var/cache/yum

WORKDIR /thirdparty
RUN curl -L https://github.com/GNOME/gtk/archive/gtk-3-0.zip --output gtk-3-0.zip && \
    curl -L https://archive.kernel.org/centos-vault/8.1.1911/BaseOS/Source/SPackages/gcc-8.3.1-4.5.el8.src.rpm --output gcc-8.3.1-4.5.el8.src.rpm

# runtime package
# for CPU

# Post-installation cleanup and setting up OpenVINO environment variables
RUN rm -rf /tmp && mkdir /tmp
RUN if [ -f "${INTEL_OPENVINO_DIR}"/bin/setupvars.sh ]; then \
        printf "\nexport TBB_DIR=\${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/tbb/cmake\n" >> ${INTEL_OPENVINO_DIR}/bin/setupvars.sh; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /home/openvino/.bashrc; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /root/.bashrc; \
    fi;

USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers below
