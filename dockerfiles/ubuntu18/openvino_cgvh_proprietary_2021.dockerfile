# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:18.04 AS base

# hadolint ignore=DL3002
USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* && ln -snf /usr/share/zoneinfo/$(curl https://ipapi.co/timezone -k) /etc/localtime

# download source for pypi-kenlm LGPL package
WORKDIR /tmp
RUN curl -L https://files.pythonhosted.org/packages/7f/e6/1639d2de28c27632e3136015ecfd67774cca6f55146507baeaef06b113ba/pypi-kenlm-0.1.20190403.tar.gz --output pypi-kenlm.tar.gz

# download source for LGPL packages
WORKDIR /thirdparty

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://salsa.debian.org/toolchain-team/gcc-defaults.git && \
    curl -L https://github.com/GNOME/gtk/archive/gtk-3-0.zip --output gtk-3-0.zip && \
    git clone https://git.launchpad.net/~ubuntu-core-dev/ubuntu/+source/glibc && \
    curl -L https://github.com/GStreamer/gstreamer/archive/1.0.zip --output gstreamer1.0.zip && \
    curl -L https://github.com/GStreamer/gst-plugins-base/archive/1.0.zip --output gst-plugins-base1.0.zip && \
    curl -L https://github.com/GStreamer/gst-plugins-good/archive/1.0.zip --output gst-plugins-good1.0.zip && \
    curl -L https://github.com/GStreamer/gst-plugins-bad/archive/1.0.zip --output gst-plugins-bad1.0.zip && \
    curl -L https://github.com/GStreamer/gstreamer-vaapi/archive/master.zip --output gstreamer-vaapi.zip && \
    curl -L https://github.com/FFmpeg/FFmpeg/archive/master.zip --output ffmpeg.zip


WORKDIR /tmp
# download source for udev LGPL package
RUN curl -L https://github.com/systemd/systemd/archive/master.zip --output systemd.zip


# get product from URL
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}

# install product by installation script
ENV INTEL_OPENVINO_DIR /opt/intel/openvino

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends cpio && \
    rm -rf /var/lib/apt/lists/* && \
    tar -xzf ${TEMP_DIR}/*.tgz --strip 1 && \
    sed -i 's/decline/accept/g' silent.cfg && \
    ${TEMP_DIR}/install.sh -s silent.cfg && \
    OV_BUILD="$(find /opt/intel -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d+')" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && rm -rf ${TEMP_DIR} && \
    rm -rf ${INTEL_OPENVINO_DIR}/deployment_tools/tools/workbench



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

LABEL Description="This is the proprietary image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL Vendor="Intel Corporation"

USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino

RUN mkdir /opt/intel

ENV INTEL_OPENVINO_DIR /opt/intel/openvino

COPY --from=base /opt/intel /opt/intel

WORKDIR /thirdparty
COPY --from=base /thirdparty /thirdparty


ARG DEPS="dpkg-dev \
          libopenexr22 \
          flex"
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
               libglib2.0"


# hadolint ignore=DL3008
RUN sed -Ei 's/# deb-src /deb-src /' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y curl && ln -snf /usr/share/zoneinfo/$(curl https://ipapi.co/timezone -k) /etc/localtime && \
    apt-get install -y --no-install-recommends ${DEPS} ${LGPL_DEPS} && \
    apt-get source --download-only ${LGPL_DEPS} || true && \
    rm -rf /var/lib/apt/lists/*


# setup Python
ENV PYTHON_VER python3.6


# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip python3-dev python3-venv python3-setuptools lib${PYTHON_VER} && \
    rm -rf /var/lib/apt/lists/*


RUN ${PYTHON_VER} -m pip install --upgrade pip

# proprietary package
WORKDIR /tmp

RUN ${PYTHON_VER} -m pip install --no-cache-dir cmake && \
    ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/python/${PYTHON_VER}/requirements.txt && \
    find "${INTEL_OPENVINO_DIR}/" -type f \( -name "*requirements.*" -o  -name "*requirements_ubuntu18.*" -o \( -name "*requirements*.in" -and -not -name "*requirements-tensorflow.in" \) \) -not -path "*/accuracy_checker/*" -not -path "*/post_training_optimization_toolkit/*" -not -path "*/python3*/*" -not -path "*/python2*/*" -print -exec ${PYTHON_VER} -m pip install --no-cache-dir -r "{}" \;

ENV VENV_TF2 /opt/intel/venv_tf2

RUN ${PYTHON_VER} -m venv ${VENV_TF2} && \
    source ${VENV_TF2}/bin/activate && \
    pip install --no-cache-dir -U pip==19.3.1 && \
    pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/model_optimizer/requirements_tf2.txt && \
    pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/downloader/requirements-tensorflow.in && \
    deactivate


WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker
RUN source ${INTEL_OPENVINO_DIR}/bin/setupvars.sh && \
    ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/requirements.in && \
    ${PYTHON_VER} ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/setup.py install && \
    rm -rf ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/build

COPY --from=base /tmp/pypi-kenlm.tar.gz /thirdparty/pypi-kenlm.tar.gz

WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit
RUN ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/requirements.txt && \
    ${PYTHON_VER} ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/setup.py install && \
    rm -rf ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/build

# for CPU

# for GPU
ARG TEMP_DIR=/tmp/opencl

COPY --from=base ${TEMP_DIR} ${TEMP_DIR}

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends ocl-icd-libopencl1 && \
    rm -rf /var/lib/apt/lists/* && \
    dpkg -i ${TEMP_DIR}/*.deb && \
    ldconfig && \
    rm -rf ${TEMP_DIR}

# for VPU
ARG DEPENDENCIES=udev

WORKDIR /thirdparty
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

COPY --from=base /opt/libusb-1.0.22 /opt/libusb-1.0.22

# download source for udev LGPL package
COPY --from=base /tmp/systemd.zip /thirdparty/systemd.zip

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
        printf "\nexport LIBVA_DRIVER_NAME=iHD \nexport LIBVA_DRIVERS_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/ \nexport GST_VAAPI_ALL_DRIVERS=1 \nexport LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LIBRARY_PATH \nexport LD_LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LD_LIBRARY_PATH \n" >> /home/openvino/.bashrc; \
        printf "\nexport LIBVA_DRIVER_NAME=iHD \nexport LIBVA_DRIVERS_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/ \nexport GST_VAAPI_ALL_DRIVERS=1 \nexport LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LIBRARY_PATH \nexport LD_LIBRARY_PATH=\${INTEL_OPENVINO_DIR}/opt/intel/mediasdk/lib64/:\$LD_LIBRARY_PATH \n" >> /root/.bashrc; \
    fi;

RUN apt-get update && \
    apt-get autoremove -y dpkg-dev && \
    apt-get install -y --no-install-recommends ${LGPL_DEPS} && \
    rm -rf /var/lib/apt/lists/*

USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers below
