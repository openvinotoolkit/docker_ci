# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:20.04 as ov_base

# hadolint ignore=DL3002
USER root

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      python3-minimal \
      python3-setuptools \
      python3-pip && \
      rm -rf /var/lib/apt/lists/*

# get product from URL
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}
ARG build_id
# install product by copying archive content
ARG TEMP_DIR=/tmp/openvino_installer
ENV INTEL_OPENVINO_DIR /opt/intel/openvino

RUN tar -xzf "${TEMP_DIR}"/*.tgz && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d.\d+')" && \
    OV_YEAR="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino_"$OV_YEAR" && \
    rm -rf ${INTEL_OPENVINO_DIR}/tools/workbench && rm -rf ${TEMP_DIR}


# Install Python and some dependencies for deployment manager
# hadolint ignore=DL3013
RUN pip3 install --no-cache-dir pytest-shutil

# Create CPU only package
RUN mkdir openvino_pkg
RUN /bin/bash -c "source /opt/intel/openvino_2022/setupvars.sh" && \
    python3 /opt/intel/openvino_2022/tools/deployment_manager/deployment_manager.py \
        --targets cpu \
        --output_dir openvino_pkg \
        --archive_name openvino_deploy_package

RUN cp -r /opt/intel/openvino_2022/runtime/cmake . && \
    cp -r /opt/intel/openvino_2022/runtime/include . && \
    cp -r /opt/intel/openvino_2022/runtime/lib/intel64/libopenvino_tensorflow_fe.so .

# Replace full package by CPU package
RUN rm -r /opt/intel/ && mkdir -p "/opt/intel/openvino_${build_id}" && \
    tar -xf "${TEMP_DIR}"/openvino_pkg/openvino_deploy_package.tar.gz -C "/opt/intel/openvino_${build_id}" && \
    ln --symbolic "/opt/intel/openvino_${build_id}" /opt/intel/openvino_2022 && \
    ln --symbolic "/opt/intel/openvino_${build_id}" /opt/intel/openvino && \
    mv "${TEMP_DIR}"/cmake /opt/intel/openvino_2022/runtime/cmake && \
    mv "${TEMP_DIR}"/include /opt/intel/openvino_2022/runtime/include && \
    mv "${TEMP_DIR}"/libopenvino_tensorflow_fe.so /opt/intel/openvino_2022/runtime/lib/intel64

FROM ubuntu:20.04

LABEL description="This is the base CPU only image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 20.04 LTS"
LABEL vendor="Intel Corporation"

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

COPY --from=ov_base /opt/intel /opt/intel
RUN echo "source /opt/intel/openvino_2022/setupvars.sh" | tee -a /root/.bashrc

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      g++ \
      python3 \
      cmake \
      make && \
      rm -rf /var/lib/apt/lists/*

# Creating user openvino
RUN useradd -ms /bin/bash -G users openvino && \
    chown openvino -R /home/openvino

USER openvino

RUN echo "source /opt/intel/openvino_2022/setupvars.sh" | tee -a /home/openvino/.bashrc

WORKDIR /opt/intel/openvino

CMD ["/bin/bash"]
