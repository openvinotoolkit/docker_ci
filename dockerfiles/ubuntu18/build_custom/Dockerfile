# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:18.04 AS setup_openvino

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

# hadolint ignore=DL3008
RUN apt-get update; \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        apt-utils \
        git \
        git-lfs \
        ca-certificates \
        sudo \
        tzdata; \
    rm -rf /var/lib/apt/lists/*

ARG OPENVINO_FORK="openvinotoolkit"
ARG OPENVINO_BRANCH="master"

RUN git-lfs install; \
    git clone https://github.com/${OPENVINO_FORK}/openvino.git \
    --recurse-submodules --shallow-submodules --depth 1 -b ${OPENVINO_BRANCH} /opt/intel/repo/openvino

WORKDIR /opt/intel/repo/openvino
RUN chmod +x install_build_dependencies.sh; \
    ./install_build_dependencies.sh

ARG OCL_VERSION="19.41.14441"

RUN chmod +x scripts/install_dependencies/install_NEO_OCL_driver.sh; \
    ./scripts/install_dependencies/install_NEO_OCL_driver.sh -y --no_numa -d ${OCL_VERSION}

# hadolint ignore=DL3013
RUN chmod +x scripts/install_dependencies/install_openvino_dependencies.sh; \
    ./scripts/install_dependencies/install_openvino_dependencies.sh -y -c=python; \
    python3 -m pip install --no-cache-dir --upgrade pip; \
    python3 -m pip install --no-cache-dir -r inference-engine/ie_bridges/python/src/requirements-dev.txt

WORKDIR /opt/intel/repo
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM setup_openvino AS build_openvino

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

COPY openvino_cmake.txt /opt/intel/repo

WORKDIR /opt/intel/repo/openvino/build
# hadolint ignore=SC2046
RUN cmake $(cat /opt/intel/repo/openvino_cmake.txt) /opt/intel/repo/openvino; \
    make "-j$(nproc)"; \
    make install

WORKDIR /tmp
RUN curl -L https://github.com/libusb/libusb/archive/v1.0.22.zip --output v1.0.22.zip; \
    unzip v1.0.22.zip; \
    rm -rf v1.0.22.zip

WORKDIR /tmp/libusb-1.0.22
RUN ./bootstrap.sh; \
    ./configure --disable-udev --enable-shared; \
    make "-j$(nproc)"

WORKDIR /opt/intel/repo
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM ubuntu:18.04 AS copy_openvino

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

ENV INTEL_OPENVINO_DIR="/opt/intel/openvino"

COPY --from=build_openvino /opt/intel/repo /opt/intel/repo
RUN rm -rf /opt/intel/repo/openvino/build/install
COPY --from=build_openvino /opt/intel/repo/openvino/build/install ${INTEL_OPENVINO_DIR}
COPY --from=build_openvino /tmp/libusb-1.0.22 /opt/libusb-1.0.22

WORKDIR ${INTEL_OPENVINO_DIR}
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM copy_openvino AS openvino

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

# hadolint ignore=DL3008
RUN apt-get update; \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        apt-utils \
        wget \
        udev \
        sudo \
        gdb \
        tzdata; \
    rm -rf /var/lib/apt/lists/*

WORKDIR ${INTEL_OPENVINO_DIR}
RUN chmod +x install_dependencies/install_openvino_dependencies.sh; \
    ./install_dependencies/install_openvino_dependencies.sh -y -c=python -c=dev

ARG OCL_VERSION="19.41.14441"

RUN chmod +x install_dependencies/install_NEO_OCL_driver.sh; \
    ./install_dependencies/install_NEO_OCL_driver.sh -y --no_numa -d ${OCL_VERSION}

WORKDIR /opt/libusb-1.0.22
RUN ./libtool --mode=install install -c libusb/libusb-1.0.la /usr/local/lib/; \
    mkdir -p /usr/local/include/libusb-1.0; \
    install -c -m 644 libusb/libusb.h /usr/local/include/libusb-1.0; \
    mkdir -p /usr/local/lib/pkgconfig; \
    install -c -m 644 libusb-1.0.pc /usr/local/lib/pkgconfig

WORKDIR ${INTEL_OPENVINO_DIR}
RUN chmod +x install_dependencies/install_NCS_udev_rules.sh; \
    ./install_dependencies/install_NCS_udev_rules.sh

# hadolint ignore=DL3013
RUN python3 -m pip install --no-cache-dir --upgrade pip; \
    python3 -m pip install --no-cache-dir -r python/python3.6/requirements.txt; \
    python3 -m pip install --no-cache-dir -r tools/model_optimizer/requirements.txt

RUN printf "\nsource \${INTEL_OPENVINO_DIR}/setupvars.sh\n" >> /root/.bashrc

CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM openvino AS opencv

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        git \
        libva-dev \
        libgtk-3-dev \
        libavcodec-dev \
        libavformat-dev \
        libavutil-dev \
        libswscale-dev \
        libavresample-dev \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev \
        libgstreamer-plugins-good1.0-dev \
        libgstreamer-plugins-bad1.0-dev; \
    rm -rf /var/lib/apt/lists/*

ARG OPENCV_BRANCH="master"

WORKDIR /opt/intel/repo
RUN git clone https://github.com/opencv/opencv.git --depth 1 -b ${OPENCV_BRANCH}

COPY opencv_cmake.txt /opt/intel/repo

WORKDIR /opt/intel/repo/opencv/build
# hadolint ignore=SC2046
RUN . "${INTEL_OPENVINO_DIR}/setupvars.sh"; \
    cmake $(cat /opt/intel/repo/opencv_cmake.txt) /opt/intel/repo/opencv; \
    make "-j$(nproc)"; \
    make install

WORKDIR /opt/intel/repo/opencv/build/install
RUN mkdir "${INTEL_OPENVINO_DIR}/extras"; \
    cp -r . "${INTEL_OPENVINO_DIR}/extras/opencv"; \
    cp -r "${INTEL_OPENVINO_DIR}/extras/opencv/python/python3" "${INTEL_OPENVINO_DIR}/python"; \
    rm -r "${INTEL_OPENVINO_DIR}/extras/opencv/python"; \
    echo "export OpenCV_DIR=${INTEL_OPENVINO_DIR}/extras/opencv/cmake" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"; \
    echo "export LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/extras/opencv/lib:\$LD_LIBRARY_PATH" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"; \
    rm -rf /opt/intel/repo/opencv/build/install

WORKDIR ${INTEL_OPENVINO_DIR}
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM opencv AS open_model_zoo

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

ARG OMZ_BRANCH="master"

WORKDIR ${INTEL_OPENVINO_DIR}/extras
RUN git clone https://github.com/openvinotoolkit/open_model_zoo.git --recurse-submodules --shallow-submodules --depth 1 -b ${OMZ_BRANCH}; \
    python3 -m pip install --no-cache-dir -r open_model_zoo/tools/accuracy_checker/requirements.in; \
    python3 -m pip install --no-cache-dir -r open_model_zoo/tools/model_tools/requirements.in; \
    python3 -m pip install --no-cache-dir -r open_model_zoo/tools/model_tools/requirements-caffe2.in; \
    python3 -m pip install --no-cache-dir -r open_model_zoo/tools/model_tools/requirements-pytorch.in; \
    python3 -m pip install --no-cache-dir -r open_model_zoo/tools/model_tools/requirements-tensorflow.in

WORKDIR ${INTEL_OPENVINO_DIR}/extras/open_model_zoo/tools/accuracy_checker
RUN python3 "${INTEL_OPENVINO_DIR}"/extras/open_model_zoo/tools/accuracy_checker/setup.py install && \
    rm -rf "${INTEL_OPENVINO_DIR}"/extras/open_model_zoo/tools/accuracy_checker/build

WORKDIR ${INTEL_OPENVINO_DIR}/extras/open_model_zoo/tools/model_tools
RUN . "${INTEL_OPENVINO_DIR}/setupvars.sh" && \
    python3 "${INTEL_OPENVINO_DIR}"/extras/open_model_zoo/tools/model_tools/setup.py install && \
    rm -rf "${INTEL_OPENVINO_DIR}"/extras/open_model_zoo/tools/model_tools/build && \
    if [ -d "${INTEL_OPENVINO_DIR}/extras/opencv" ]; then python3 -m pip uninstall -y opencv-python; fi

WORKDIR ${INTEL_OPENVINO_DIR}
CMD ["/bin/bash"]