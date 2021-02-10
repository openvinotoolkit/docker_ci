# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:18.04 as base

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      gnupg \
      python3-minimal \
      python3-pip

ARG PUBLIC_KEY="https://apt.repos.intel.com/openvino/2020/GPG-PUB-KEY-INTEL-OPENVINO-2020"
ARG APT_REPOSITORY="deb https://apt.repos.intel.com/openvino/2020 all main"
ARG BUILD_ID
# Install full package
RUN curl -o GPG-PUB-KEY-INTEL-OPENVINO-2020 ${PUBLIC_KEY} && \
    apt-key add GPG-PUB-KEY-INTEL-OPENVINO-2020 && \
    echo ${APT_REPOSITORY} | tee - a /etc/apt/sources.list.d/intel-openvino-2020.list && \
    apt-get update && apt-get install -y --no-install-recommends "intel-openvino-dev-ubuntu18-${BUILD_ID}" && \
    rm -rf /var/lib/apt/lists/*

# Install Python and some dependencies
RUN pip3 install setuptools
RUN pip3 install pytest-shutil

# Create CPU only package
RUN mkdir openvino_pkg
RUN /bin/bash -c "source /opt/intel/openvino/bin/setupvars.sh" && \
    python3 /opt/intel/openvino/deployment_tools/tools/deployment_manager/deployment_manager.py \
        --targets cpu \
        --output_dir openvino_pkg \
        --archive_name openvino_deploy_package

RUN cp -r /opt/intel/openvino/deployment_tools/inference_engine/share . && \
    cp -r /opt/intel/openvino/deployment_tools/inference_engine/include . && \
    cp -r /opt/intel/openvino/licensing . && \
    cp /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libinference_engine_c_api.so . && \
    cp /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libinference_engine_nn_builder.so .

# Replace full package by CPU package
RUN rm -r /opt/intel/ && mkdir -p "/opt/intel/openvino_${BUILD_ID}" && \
    tar -xf /openvino_pkg/openvino_deploy_package.tar.gz --strip 1 -C "/opt/intel/openvino_${BUILD_ID}" && \
    ln --symbolic "/opt/intel/openvino_${BUILD_ID}" /opt/intel/openvino && \
    mv /share /opt/intel/openvino/deployment_tools/inference_engine/share && \
    mv /include /opt/intel/openvino/deployment_tools/inference_engine/include && \
    mv /licensing /opt/intel/openvino/licensing && \
    mv /libinference_engine_c_api.so /libinference_engine_nn_builder.so /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/

FROM ubuntu:18.04

LABEL Description="This is the base CPU only image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL Vendor="Intel Corporation"

COPY --from=base /opt/intel /opt/intel
RUN echo "source /opt/intel/openvino/bin/setupvars.sh" | tee -a /root/.bashrc

# Creating user openvino
RUN useradd -ms /bin/bash -G users openvino && \
    chown openvino -R /home/openvino

USER openvino

RUN echo "source /opt/intel/openvino/bin/setupvars.sh" | tee -a /home/openvino/.bashrc

WORKDIR /opt/intel/openvino

CMD ["/bin/bash"]