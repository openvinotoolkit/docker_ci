# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:20.04 as ov_base

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      gnupg \
      python3-minimal \
      python3-setuptools \
      python3-pip && \
      rm -rf /var/lib/apt/lists/*

ARG build_id
# Install full package
RUN curl -o GPG-PUB-KEY-INTEL-OPENVINO-2021 https://apt.repos.intel.com/openvino/2021/GPG-PUB-KEY-INTEL-OPENVINO-2021 && \
    apt-key add GPG-PUB-KEY-INTEL-OPENVINO-2021 && \
    echo "deb https://apt.repos.intel.com/openvino/2021 all main" | tee - a /etc/apt/sources.list.d/intel-openvino-2021.list && \
    apt-get update && apt-get install -y --no-install-recommends intel-openvino-dev-ubuntu20-"${build_id}" && \
    rm -rf /var/lib/apt/lists/*

# Install Python and some dependencies for deployment manager
RUN pip3 install pytest-shutil

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
RUN rm -r /opt/intel/ && mkdir -p /opt/intel/openvino_"${build_id}" && \
    tar -xf /openvino_pkg/openvino_deploy_package.tar.gz -C /opt/intel/openvino_"${build_id}" && \
    ln --symbolic /opt/intel/openvino_"${build_id}"/ /opt/intel/openvino_2021 && \
    ln --symbolic /opt/intel/openvino_"${build_id}"/ /opt/intel/openvino && \
    mv setupvars.sh /opt/intel/openvino_2021/bin && \
    mv /licensing /opt/intel/openvino_2021/licensing && \
    mv /share /opt/intel/openvino_2021/deployment_tools/inference_engine/share && \
    mv /include /opt/intel/openvino_2021/deployment_tools/inference_engine/include && \
    mv /libinference_engine_c_api.so /opt/intel/openvino_2021/deployment_tools/inference_engine/lib/intel64/ && \
    mv /ngraph_cmake /opt/intel/openvino_2021/deployment_tools/ngraph/cmake && \
    mv /ngraph_include /opt/intel/openvino_2021/deployment_tools/ngraph/include

FROM ubuntu:20.04

LABEL Description="This is the base CPU only image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 20.04 LTS"
LABEL Vendor="Intel Corporation"

COPY --from=ov_base /opt/intel /opt/intel

RUN echo "source /opt/intel/openvino_2021/bin/setupvars.sh" | tee -a /root/.bashrc

# Creating user openvino
RUN useradd -ms /bin/bash -G users openvino && \
    chown openvino -R /home/openvino

USER openvino

RUN echo "source /opt/intel/openvino_2021/bin/setupvars.sh" | tee -a /home/openvino/.bashrc

WORKDIR /opt/intel/openvino

CMD ["/bin/bash"]
