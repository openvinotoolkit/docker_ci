# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:18.04 AS base

# hadolint ignore=DL3002
USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tzdata ca-certificates && \
    rm -rf /var/lib/apt/lists/*


# get product from URL
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}

# install product by copying archive content
ARG TEMP_DIR=/tmp/openvino_installer
ENV INTEL_OPENVINO_DIR /opt/intel/openvino

# Creating user openvino and adding it to groups"users"
RUN useradd -ms /bin/bash -G users openvino

RUN tar -xzf "${TEMP_DIR}"/*.tgz && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d.\d+')" && \
    OV_YEAR="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino_"$OV_YEAR" && \
    rm -rf ${INTEL_OPENVINO_DIR}/tools/workbench && rm -rf ${TEMP_DIR} && \
    chown -R openvino /opt/intel/openvino_"$OV_BUILD"


ENV HDDL_INSTALL_DIR=/opt/intel/openvino/runtime/3rdparty/hddl
ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python/python3.8:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino
ENV PKG_CONFIG_PATH=/opt/intel/openvino/runtime/lib/intel64/pkgconfig

# for VPU
ARG BUILD_DEPENDENCIES="autoconf \
                        automake \
                        build-essential \
                        libtool \
                        unzip"

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends ${BUILD_DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN curl -L https://github.com/libusb/libusb/archive/v1.0.22.zip --output v1.0.22.zip && \
    unzip v1.0.22.zip && rm -rf v1.0.22.zip

WORKDIR /opt/libusb-1.0.22
RUN ./bootstrap.sh && \
    ./configure --disable-udev --enable-shared && \
    make -j4

RUN rm -rf ${INTEL_OPENVINO_DIR}/.distribution && mkdir ${INTEL_OPENVINO_DIR}/.distribution && \
    touch ${INTEL_OPENVINO_DIR}/.distribution/docker
# -----------------



FROM ubuntu:18.04 AS ov_base

LABEL description="This is the runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL vendor="Intel Corporation"

USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN sed -ri -e 's@^UMASK[[:space:]]+[[:digit:]]+@UMASK 000@g' /etc/login.defs && \
	grep -E "^UMASK" /etc/login.defs && useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino

RUN mkdir /opt/intel

ENV INTEL_OPENVINO_DIR /opt/intel/openvino

COPY --from=base /opt/intel /opt/intel

WORKDIR /thirdparty

ARG INSTALL_SOURCES="no"

ARG DEPS="tzdata \
          curl"

ARG LGPL_DEPS=
ARG INSTALL_PACKAGES="-c=opencv_req -c=python -c=cl_compiler -c=core"


# hadolint ignore=DL3008
RUN apt-get update && \
    dpkg --get-selections | grep -v deinstall | awk '{print $1}' > base_packages.txt  && \
    apt-get install -y --no-install-recommends ${DEPS} && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates
RUN curl https://raw.githubusercontent.com/openvinotoolkit/openvino/master/scripts/install_dependencies/install_openvino_dependencies.sh -o ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh && \
    chmod 775 ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh

# hadolint ignore=DL3008, SC2012
RUN apt-get update && \
    apt-get install -y --no-install-recommends ${LGPL_DEPS} && \
    ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh -y ${INSTALL_PACKAGES} && \
    if [ "$INSTALL_SOURCES" = "yes" ]; then \
      sed -Ei 's/# deb-src /deb-src /' /etc/apt/sources.list && \
      apt-get update && \
	  dpkg --get-selections | grep -v deinstall | awk '{print $1}' > all_packages.txt && \
	  grep -v -f base_packages.txt all_packages.txt | while read line; do \
	  package=$(echo $line); \
	  name=(${package//:/ }); \
      grep -l GPL /usr/share/doc/${name[0]}/copyright; \
      exit_status=$?; \
	  if [ $exit_status -eq 0 ]; then \
	    apt-get source -q --download-only $package;  \
	  fi \
      done && \
      echo "Download source for $(ls | wc -l) third-party packages: $(du -sh)"; fi && \
    rm /usr/lib/python3.*/lib-dynload/readline.cpython-3*-gnu.so && rm -rf /var/lib/apt/lists/*

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN if [ "$INSTALL_SOURCES" = "no" ]; then \
        echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. They are stored in https://storage.openvinotoolkit.org/repositories/openvino/ci_dependencies/container_gpl_sources/." > DockerImage_readme.txt ; \
    fi


ENV HDDL_INSTALL_DIR=/opt/intel/openvino/runtime/3rdparty/hddl
ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python/python3.8:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino
ENV PKG_CONFIG_PATH=/opt/intel/openvino/runtime/lib/intel64/pkgconfig

# setup Python
ENV PYTHON_VER python3.8

RUN ${PYTHON_VER} -m pip install --upgrade pip setuptools
RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python3.8 2

# runtime package
WORKDIR ${INTEL_OPENVINO_DIR}
ARG OPENVINO_WHEELS_VERSION=2022.3.0
ARG OPENVINO_WHEELS_URL
RUN ${PYTHON_VER} -m pip install --no-cache-dir cmake && \
    if [ -z "$OPENVINO_WHEELS_URL" ]; then \
        ${PYTHON_VER} -m pip install --no-cache-dir openvino=="$OPENVINO_WHEELS_VERSION" ; \
    else \
        ${PYTHON_VER} -m pip install --no-cache-dir --pre openvino=="$OPENVINO_WHEELS_VERSION" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" ; \
    fi

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
# Please use `third-party-programs-docker-runtime.txt` short path to 3d party file if you use the Dockerfile directly from docker_ci/dockerfiles repo folder
COPY dockerfiles/ubuntu18/third-party-programs-docker-runtime.txt ${INTEL_OPENVINO_DIR}/licensing

# for CPU

# for GPU
ARG TEMP_DIR=/tmp/opencl

WORKDIR ${INTEL_OPENVINO_DIR}/install_dependencies
RUN ./install_NEO_OCL_driver.sh --no_numa -y && \
    rm -rf /var/lib/apt/lists/*

# for VPU
ARG LGPL_DEPS=udev

WORKDIR /thirdparty

# hadolint ignore=DL3008, SC2012
RUN apt-get update && \
    dpkg --get-selections | grep -v deinstall | awk '{print $1}' > no_vpu_packages.txt && \
    apt-get install -y --no-install-recommends ${LGPL_DEPS} && \
    if [ "$INSTALL_SOURCES" = "yes" ]; then \
      sed -Ei 's/# deb-src /deb-src /' /etc/apt/sources.list && \
      apt-get update && \
	  dpkg --get-selections | grep -v deinstall | awk '{print $1}' > vpu_packages.txt && \
	  grep -v -f no_vpu_packages.txt vpu_packages.txt | while read line; do \
	  package=$(echo $line); \
	  name=(${package//:/ }); \
      grep -l GPL /usr/share/doc/${name[0]}/copyright; \
      exit_status=$?; \
	  if [ $exit_status -eq 0 ]; then \
	    apt-get source -q --download-only $package;  \
	  fi \
      done && \
      echo "Download source for $(ls | wc -l) third-party packages: $(du -sh)"; fi && \
    rm -rf /var/lib/apt/lists/*

COPY --from=base /opt/libusb-1.0.22 /opt/libusb-1.0.22

# libglib2.0-dev package that is required to build dl_streamer samples
WORKDIR /opt/libusb-1.0.22/libusb
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils && \
    /bin/mkdir -p '/usr/local/lib' && \
    /bin/bash ../libtool   --mode=install /usr/bin/install -c   libusb-1.0.la '/usr/local/lib' && \
    /bin/mkdir -p '/usr/local/include/libusb-1.0' && \
    /usr/bin/install -c -m 644 libusb.h '/usr/local/include/libusb-1.0' && \
    /bin/mkdir -p '/usr/local/lib/pkgconfig' &&\
    apt-get autoremove -y binutils && \
    apt-get install libglib2.0-dev g++ -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/libusb-1.0.22/
RUN /usr/bin/install -c -m 644 libusb-1.0.pc '/usr/local/lib/pkgconfig' && \
    cp ${INTEL_OPENVINO_DIR}/install_dependencies/97-myriad-usbboot.rules /etc/udev/rules.d/ && \
    ldconfig

# for HDDL
WORKDIR /tmp
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libboost-filesystem1.65-dev \
        libboost-program-options1.65-dev \
        libboost-thread1.65-dev \
        libjson-c3 libxxf86vm-dev && \
    rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*


USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}
ENV DEBIAN_FRONTEND=noninteractive

CMD ["/bin/bash"]

# Setup custom layers below
