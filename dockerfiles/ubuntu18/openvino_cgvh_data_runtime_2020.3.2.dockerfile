# Copyright (C) 2019-2021 Intel Corporation
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



# for GPU
ARG GMMLIB
ARG IGC_CORE
ARG IGC_OPENCL
ARG INTEL_OPENCL
ARG INTEL_OCLOC
ARG TEMP_DIR=/tmp/opencl

WORKDIR ${TEMP_DIR}
RUN curl -L "https://github.com/intel/compute-runtime/releases/download/${INTEL_OPENCL}/intel-gmmlib_${GMMLIB}_amd64.deb" --output "intel-gmmlib_${GMMLIB}_amd64.deb" && \
    curl -L "https://github.com/intel/compute-runtime/releases/download/${INTEL_OPENCL}/intel-igc-core_${IGC_CORE}_amd64.deb" --output "intel-igc-core_${IGC_CORE}_amd64.deb" && \
    curl -L "https://github.com/intel/compute-runtime/releases/download/${INTEL_OPENCL}/intel-igc-opencl_${IGC_OPENCL}_amd64.deb" --output "intel-igc-opencl_${IGC_OPENCL}_amd64.deb" && \
    curl -L "https://github.com/intel/compute-runtime/releases/download/${INTEL_OPENCL}/intel-opencl_${INTEL_OPENCL}_amd64.deb" --output "intel-opencl_${INTEL_OPENCL}_amd64.deb" && \
    curl -L "https://github.com/intel/compute-runtime/releases/download/${INTEL_OPENCL}/intel-ocloc_${INTEL_OCLOC}_amd64.deb" --output "intel-ocloc_${INTEL_OCLOC}_amd64.deb"


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

# -----------------
FROM ubuntu:18.04 AS ov_base

LABEL Description="This is the data_runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL Vendor="Intel Corporation"

USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino

RUN mkdir /opt/intel

ENV INTEL_OPENVINO_DIR /opt/intel/openvino

COPY --from=base /opt/intel /opt/intel

WORKDIR /thirdparty

ARG INSTALL_SOURCES="no"



ARG DEPS="tzdata \
          curl \
          libgl1 \
          libtinfo5 \
          libopenexr22 \
          flex \
          vainfo"
ARG LGPL_DEPS="g++ \
               gcc \
               libc6-dev \
               libgtk-3-0 \
               libgstreamer1.0-0 \
               gstreamer1.0-plugins-base \
               gstreamer1.0-plugins-good \
               gstreamer1.0-plugins-bad \
               gstreamer1.0-vaapi \
               ffmpeg \
               libgl-dev \
               libtag-extras1 \
               libfaac0 \
               python3-gi \
               libfluidsynth1 \
               libnettle6 \
               gstreamer1.0-plugins-ugly \
               gstreamer1.0-alsa \
               libglib2.0-dev \
               gstreamer1.0-tools"



# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends dpkg-dev && \
    dpkg --get-selections | grep -v deinstall | awk '{print $1}' > base_packages.txt  && \
    apt-get install -y --no-install-recommends ${DEPS} && \
    rm -rf /var/lib/apt/lists/*


# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends ${LGPL_DEPS} && \
    if [ "$INSTALL_SOURCES" = "yes" ]; then \
      sed -Ei 's/# deb-src /deb-src /' /etc/apt/sources.list && \
      apt-get update && \
	  dpkg --get-selections | grep -v deinstall | awk '{print $1}' > all_packages.txt && \
	  grep -v -f base_packages.txt all_packages.txt | while read line; do \
	  package=`echo $line`; \
	  name=(${package//:/ }); \
      grep -l GPL /usr/share/doc/${name[0]}/copyright; \
      exit_status=$?; \
	  if [ $exit_status -eq 0 ]; then \
	    apt-get source -q --download-only $package;  \
	  fi \
      done && \
      echo "Download source for `ls | wc -l` third-party packages: `du -sh`"; fi && \
    rm -rf /var/lib/apt/lists/*


WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN if [ "$INSTALL_SOURCES" = "no" ]; then \
        echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. Please use tag <YYYY.U_src> to pull the image with downloaded sources." > DockerImage_readme.txt ; \
    fi


# setup Python
ENV PYTHON_VER python3.6



# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools lib${PYTHON_VER} && \
    rm -rf /var/lib/apt/lists/*



RUN ${PYTHON_VER} -m pip install --upgrade pip

# runtime package
WORKDIR /tmp

RUN ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/python/${PYTHON_VER}/requirements.txt && \
    if [ -f ${INTEL_OPENVINO_DIR}/data_processing/dl_streamer/requirements.txt ]; then \
        ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/data_processing/dl_streamer/requirements.txt; \
    fi





# for CPU

# for GPU
ARG INTEL_OPENCL
ARG TEMP_DIR=/tmp/opencl


COPY --from=base ${TEMP_DIR} ${TEMP_DIR}

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends ocl-icd-libopencl1 && \
    dpkg -i ${TEMP_DIR}/*.deb && \
    ldconfig && \
    rm -rf ${TEMP_DIR} && \
    rm -rf /var/lib/apt/lists/*


# for VPU
ARG LGPL_DEPS=udev

WORKDIR /thirdparty

# hadolint ignore=DL3008
RUN apt-get update && \
    dpkg --get-selections | grep -v deinstall | awk '{print $1}' > no_vpu_packages.txt && \
    apt-get install -y --no-install-recommends ${LGPL_DEPS} && \
    if [ "$INSTALL_SOURCES" = "yes" ]; then \
      sed -Ei 's/# deb-src /deb-src /' /etc/apt/sources.list && \
      apt-get update && \
	  dpkg --get-selections | grep -v deinstall | awk '{print $1}' > vpu_packages.txt && \
	  grep -v -f no_vpu_packages.txt vpu_packages.txt | while read line; do \
	  package=`echo $line`; \
	  name=(${package//:/ }); \
      grep -l GPL /usr/share/doc/${name[0]}/copyright; \
      exit_status=$?; \
	  if [ $exit_status -eq 0 ]; then \
	    apt-get source -q --download-only $package;  \
	  fi \
      done && \
      echo "Download source for `ls | wc -l` third-party packages: `du -sh`"; fi && \
    rm -rf /var/lib/apt/lists/*

COPY --from=base /opt/libusb-1.0.22 /opt/libusb-1.0.22

WORKDIR /opt/libusb-1.0.22/libusb
RUN /bin/mkdir -p '/usr/local/lib' && \
    /bin/bash ../libtool   --mode=install /usr/bin/install -c   libusb-1.0.la '/usr/local/lib' && \
    /bin/mkdir -p '/usr/local/include/libusb-1.0' && \
    /usr/bin/install -c -m 644 libusb.h '/usr/local/include/libusb-1.0' && \
    /bin/mkdir -p '/usr/local/lib/pkgconfig'

WORKDIR /opt/libusb-1.0.22/
RUN /usr/bin/install -c -m 644 libusb-1.0.pc '/usr/local/lib/pkgconfig' && \
    cp ${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/97-myriad-usbboot.rules /etc/udev/rules.d/ && \
    ldconfig

# for HDDL
WORKDIR /tmp
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libboost-filesystem1.65-dev \
        libboost-thread1.65-dev \
        libjson-c3 libxxf86vm-dev && \
    rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*


# Post-installation cleanup and setting up OpenVINO environment variables
RUN if [ -f "${INTEL_OPENVINO_DIR}"/bin/setupvars.sh ]; then \
        printf "\nexport TBB_DIR=\${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/tbb/cmake\n" >> ${INTEL_OPENVINO_DIR}/bin/setupvars.sh; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /home/openvino/.bashrc; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /root/.bashrc; \
    fi; \
    if [ -d "${INTEL_OPENVINO_DIR}"/opt/intel/mediasdk ]; then \
        ln --symbolic "${INTEL_OPENVINO_DIR}"/opt/intel/mediasdk/ /opt/intel/mediasdk || true; \
        printf "\nexport LIBVA_DRIVER_NAME=iHD \nexport LIBVA_DRIVERS_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/ \nexport GST_VAAPI_ALL_DRIVERS=1 \nexport LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LIBRARY_PATH \nexport LD_LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LD_LIBRARY_PATH \n" >> /home/openvino/.bashrc; \
        printf "\nexport LIBVA_DRIVER_NAME=iHD \nexport LIBVA_DRIVERS_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/ \nexport GST_VAAPI_ALL_DRIVERS=1 \nexport LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LIBRARY_PATH \nexport LD_LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LD_LIBRARY_PATH \n" >> /root/.bashrc; \
    fi;


# "apt-get autoremove -y dpkg-dev" also removes the libglib2.0-dev package that is required to build dl_streamer samples
RUN apt-get update && \
    apt-get autoremove -y dpkg-dev && \
    apt-get install libglib2.0-dev -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*


USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers below
