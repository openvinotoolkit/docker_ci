# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:18.04 AS setup_openvino

# hadolint ignore=DL3008
RUN apt-get update; \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        git \
        git-lfs \
        ca-certificates \
        sudo \
        tzdata; \
    rm -rf /var/lib/apt/lists/*

ARG OPENVINO_BRANCH="master"

RUN git-lfs install; \
    git clone https://github.com/openvinotoolkit/openvino.git \
    --recurse-submodules --shallow-submodules --depth 1 -b ${OPENVINO_BRANCH} /tmp/openvino

WORKDIR /tmp/openvino
RUN chmod +x install_build_dependencies.sh; \
    ./install_build_dependencies.sh

ARG OCL_VERSION="19.41.14441"

RUN chmod +x scripts/install_dependencies/install_NEO_OCL_driver.sh; \
    ./scripts/install_dependencies/install_NEO_OCL_driver.sh -y --no_numa -d ${OCL_VERSION}

# hadolint ignore=DL3013
RUN chmod +x scripts/install_dependencies/install_openvino_dependencies.sh; \
    ./scripts/install_dependencies/install_openvino_dependencies.sh -y -c=python; \
    python3 -m pip install --no-cache-dir --upgrade pip; \
    python3 -m pip install --no-cache-dir -r inference-engine/ie_bridges/python/requirements.txt

WORKDIR /tmp
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM setup_openvino AS build_openvino

COPY openvino_cmake.txt /tmp

WORKDIR /tmp/openvino/build
# hadolint ignore=SC2046
RUN cmake $(cat /tmp/openvino_cmake.txt) /tmp/openvino; \
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

WORKDIR /tmp
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM ubuntu:18.04 AS copy_openvino

ENV INTEL_OPENVINO_DIR="/opt/intel/openvino"

COPY --from=build_openvino /tmp/openvino/build/install ${INTEL_OPENVINO_DIR}
COPY --from=build_openvino /tmp/libusb-1.0.22 /opt/libusb-1.0.22

WORKDIR ${INTEL_OPENVINO_DIR}
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM copy_openvino AS openvino

# hadolint ignore=DL3008
RUN apt-get update; \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        wget \
        udev \
        sudo \
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
    python3 -m pip install --no-cache-dir -r deployment_tools/model_optimizer/requirements.txt

RUN ln -s deployment_tools/inference_engine/ inference_engine
RUN printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /root/.bashrc

CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM openvino AS opencv

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        git \
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

WORKDIR /tmp
RUN git clone https://github.com/opencv/opencv.git --depth 1 -b ${OPENCV_BRANCH}

COPY opencv_cmake.txt /tmp

WORKDIR /tmp/opencv/build
# hadolint ignore=SC2046
RUN . "${INTEL_OPENVINO_DIR}/bin/setupvars.sh"; \
    cmake $(cat /tmp/opencv_cmake.txt) /tmp/opencv; \
    make "-j$(nproc)"; \
    make install

WORKDIR /tmp/opencv/build/install
RUN cp -r . "${INTEL_OPENVINO_DIR}/opencv"; \
    cp -r "${INTEL_OPENVINO_DIR}/opencv/python/python3" "${INTEL_OPENVINO_DIR}/python"; \
    rm -r "${INTEL_OPENVINO_DIR}/opencv/python"; \
    echo "export OpenCV_DIR=${INTEL_OPENVINO_DIR}/opencv/cmake" | tee -a "${INTEL_OPENVINO_DIR}/opencv/setupvars.sh"; \
    echo "export LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/opencv/lib:\$LD_LIBRARY_PATH" | tee -a "${INTEL_OPENVINO_DIR}/opencv/setupvars.sh"; \
    rm -r /tmp/*

WORKDIR ${INTEL_OPENVINO_DIR}
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------
FROM opencv AS open_model_zoo

ARG OMZ_BRANCH="master"

WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools
RUN git clone https://github.com/openvinotoolkit/open_model_zoo.git --depth 1 -b ${OMZ_BRANCH}; \
    python3 -m pip install --no-cache-dir -r open_model_zoo/tools/downloader/requirements.in; \
    ln -s ../open_model_zoo/demos inference_engine/demos

WORKDIR ${INTEL_OPENVINO_DIR}
CMD ["/bin/bash"]