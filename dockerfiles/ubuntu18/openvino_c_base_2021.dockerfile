# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:18.04 as ov_base

# hadolint ignore=DL3002
USER root

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      gnupg \
      python3-minimal \
      python3-setuptools \
      python3-pip && \
      rm -rf /var/lib/apt/lists/*

ARG PUBLIC_KEY="https://apt.repos.intel.com/openvino/2021/GPG-PUB-KEY-INTEL-OPENVINO-2021"
ARG APT_REPOSITORY="deb https://apt.repos.intel.com/openvino/2021 all main"
ARG BUILD_ID
# Install full package
RUN curl -o GPG-PUB-KEY-INTEL-OPENVINO-2021 ${PUBLIC_KEY} && \
    apt-key add GPG-PUB-KEY-INTEL-OPENVINO-2021 && \
    echo ${APT_REPOSITORY} | tee - a /etc/apt/sources.list.d/intel-openvino-2021.list && \
    apt-get update && apt-get install -y --no-install-recommends "intel-openvino-dev-ubuntu18-${BUILD_ID}" && \
    rm -rf /var/lib/apt/lists/*

# Install Python and some dependencies for deployment manager
# hadolint ignore=DL3013
RUN pip3 install --no-cache-dir pytest-shutil

# Create CPU only package
RUN mkdir openvino_pkg
RUN /bin/bash -c "source /opt/intel/openvino_2021/bin/setupvars.sh" && \
    python3 /opt/intel/openvino_2021/deployment_tools/tools/deployment_manager/deployment_manager.py \
        --targets cpu \
        --output_dir openvino_pkg \
        --archive_name openvino_deploy_package

RUN cp -r /opt/intel/openvino_2021/deployment_tools/inference_engine/share . && \
    cp -r /opt/intel/openvino_2021/deployment_tools/ngraph/cmake ngraph_cmake && \
    cp -r /opt/intel/openvino_2021/deployment_tools/ngraph/include ngraph_include && \
    cp -r /opt/intel/openvino_2021/deployment_tools/inference_engine/include . && \
    cp -r /opt/intel/openvino_2021/licensing . && \
    cp /opt/intel/openvino_2021/deployment_tools/inference_engine/lib/intel64/libinference_engine_c_api.so . && \
    cp /opt/intel/openvino_2021/bin/setupvars.sh setupvars.sh

# Replace full package by CPU package
RUN rm -r /opt/intel/ && mkdir -p "/opt/intel/openvino_${BUILD_ID}" && \
    tar -xf /openvino_pkg/openvino_deploy_package.tar.gz -C "/opt/intel/openvino_${BUILD_ID}" && \
    ln --symbolic "/opt/intel/openvino_${BUILD_ID}" /opt/intel/openvino_2021 && \
    ln --symbolic "/opt/intel/openvino_${BUILD_ID}" /opt/intel/openvino && \
    mv setupvars.sh /opt/intel/openvino_2021/bin && \
    mv /licensing /opt/intel/openvino_2021/licensing && \
    mv /share /opt/intel/openvino_2021/deployment_tools/inference_engine/share && \
    mv /include /opt/intel/openvino_2021/deployment_tools/inference_engine/include && \
    mv /libinference_engine_c_api.so /opt/intel/openvino_2021/deployment_tools/inference_engine/lib/intel64/ && \
    mv /ngraph_cmake /opt/intel/openvino_2021/deployment_tools/ngraph/cmake && \
    mv /ngraph_include /opt/intel/openvino_2021/deployment_tools/ngraph/include

FROM ubuntu:18.04

LABEL description="This is the base CPU only image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

COPY --from=ov_base /opt/intel /opt/intel
RUN echo "source /opt/intel/openvino_2021/bin/setupvars.sh" | tee -a /root/.bashrc

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      g++ \
      cmake && \
      rm -rf /var/lib/apt/lists/*

# Creating user openvino
RUN useradd -ms /bin/bash -G users openvino && \
    chown openvino -R /home/openvino

USER openvino

RUN echo "source /opt/intel/openvino_2021/bin/setupvars.sh" | tee -a /home/openvino/.bashrc

WORKDIR /opt/intel/openvino

CMD ["/bin/bash"]
