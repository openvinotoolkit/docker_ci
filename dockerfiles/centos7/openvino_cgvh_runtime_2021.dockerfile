# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM centos:7 AS base

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


# for GPU
ARG GMMLIB
ARG IGC_CORE
ARG IGC_OPENCL
ARG INTEL_OPENCL
ARG TEMP_DIR=/tmp/opencl

WORKDIR ${TEMP_DIR}
RUN curl -L https://sourceforge.net/projects/intel-compute-runtime/files/${INTEL_OPENCL}/centos-7/intel-gmmlib-${GMMLIB}-1.el7.x86_64.rpm/download -o intel-gmmlib-${GMMLIB}-1.el7.x86_64.rpm && \
    curl -L https://sourceforge.net/projects/intel-compute-runtime/files/${INTEL_OPENCL}/centos-7/intel-gmmlib-devel-${GMMLIB}-1.el7.x86_64.rpm/download -o intel-gmmlib-devel-${GMMLIB}-1.el7.x86_64.rpm && \
    curl -L https://sourceforge.net/projects/intel-compute-runtime/files/${INTEL_OPENCL}/centos-7/intel-igc-core-${IGC_CORE}-1.el7.x86_64.rpm/download -o intel-igc-core-${IGC_CORE}-1.el7.x86_64.rpm && \
    curl -L https://sourceforge.net/projects/intel-compute-runtime/files/${INTEL_OPENCL}/centos-7/intel-igc-opencl-${IGC_OPENCL}-1.el7.x86_64.rpm/download -o intel-igc-opencl-${IGC_OPENCL}-1.el7.x86_64.rpm && \
    curl -L https://sourceforge.net/projects/intel-compute-runtime/files/${INTEL_OPENCL}/centos-7/intel-igc-opencl-devel-${IGC_OPENCL}-1.el7.x86_64.rpm/download -o  intel-igc-opencl-devel-${IGC_OPENCL}-1.el7.x86_64.rpm && \
    curl -L https://sourceforge.net/projects/intel-compute-runtime/files/${INTEL_OPENCL}/centos-7/intel-opencl-${INTEL_OPENCL}-1.el7.x86_64.rpm/download -o intel-opencl-${INTEL_OPENCL}-1.el7.x86_64.rpm


# for VPU
ARG BUILD_DEPENDENCIES="autoconf \
                        automake \
                        libtool \
                        unzip"

# hadolint ignore=DL3031, DL3033
RUN yum update -y && yum install -y ${BUILD_DEPENDENCIES} && \
    yum group install -y "Development Tools" && \
    yum clean all && rm -rf /var/cache/yum

WORKDIR /opt
RUN curl -L https://github.com/libusb/libusb/archive/v1.0.22.zip --output v1.0.22.zip && \
    unzip v1.0.22.zip && rm -rf v1.0.22.zip

WORKDIR /opt/libusb-1.0.22
RUN ./bootstrap.sh && \
    ./configure --disable-udev --enable-shared && \
    make -j4

# -----------------
FROM centos:7 AS ov_base

LABEL Description="This is the runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on CentOS 7"
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

ARG LGPL_DEPS="gcc-c++ \
               gtk2"

ARG INSTALL_SOURCES="no"

WORKDIR /thirdparty
# hadolint ignore=DL3031, DL3033
RUN yum -y update && rpm -qa --qf "%{name}\n" > base_packages.txt && \
	yum install -y ${LGPL_DEPS} && \
	if [ "$INSTALL_SOURCES" = "yes" ]; then \
		rpm -qa --qf "%{name}\n" > all_packages.txt && \
		grep -v -f base_packages.txt all_packages.txt | while read line; do \
		package=`echo $line`; \
		rpm -qa $package --qf "%{name}: %{license}\n" | grep GPL; \
		exit_status=$?; \
		if [ $exit_status -eq 0 ]; then \
		    yumdownloader --source -y $package;  \
		fi \
      done && \
      echo "Download source for `ls | wc -l` third-party packages: `du -sh`"; fi && \
	yum clean all && rm -rf /var/cache/yum && rm -rf *.txt

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN if [ "$INSTALL_SOURCES" = "no" ]; then \
        echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. Please use tag <YYYY.U_src> to pull the image with downloaded sources." > DockerImage_readme.txt ; \
    fi


# setup Python
ENV PYTHON_VER python3.6

# hadolint ignore=DL3031, DL3033
RUN yum update -y && yum install -y python3 && \
    yum clean all && rm -rf /var/cache/yum

RUN ${PYTHON_VER} -m pip install --upgrade pip

# runtime package
WORKDIR /tmp

RUN ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/python/${PYTHON_VER}/requirements.txt && \
    ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/data_processing/dl_streamer/requirements.txt

# for CPU

# for GPU
ARG TEMP_DIR=/tmp/opencl

COPY --from=base ${TEMP_DIR} ${TEMP_DIR}

WORKDIR ${TEMP_DIR}

RUN groupmod -g 44 video

# hadolint ignore=DL3031, DL3033
RUN yum update -y && yum install -y epel-release && \
    yum update -y && yum install -y ocl-icd ocl-icd-devel && \ 
    yum clean all && rm -rf /var/cache/yum && \
    rpm -ivh ${TEMP_DIR}/*.rpm && \
    ldconfig && \
    rm -rf ${TEMP_DIR} && \
    yum remove -y epel-release

# for VPU
ARG DEPENDENCIES=udev

# hadolint ignore=DL3031, DL3033
RUN yum update -y && yum install -y ${DEPENDENCIES} && \
    yum clean all && rm -rf /var/cache/yum

COPY --from=base /opt/libusb-1.0.22 /opt/libusb-1.0.22

WORKDIR /opt/libusb-1.0.22/libusb
RUN /bin/mkdir -p '/usr/local/lib' && \
    /bin/bash ../libtool   --mode=install /usr/bin/install -c   libusb-1.0.la '/usr/local/lib' && \
    /bin/mkdir -p '/usr/local/include/libusb-1.0' && \
    /usr/bin/install -c -m 644 libusb.h '/usr/local/include/libusb-1.0' && \
    /bin/mkdir -p '/usr/local/lib/pkgconfig' && \
    printf "\nexport LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:/usr/local/lib\n" >> ${INTEL_OPENVINO_DIR}/bin/setupvars.sh

WORKDIR /opt/libusb-1.0.22/
RUN /usr/bin/install -c -m 644 libusb-1.0.pc '/usr/local/lib/pkgconfig' && \
    cp ${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/97-myriad-usbboot.rules /etc/udev/rules.d/ && \
    ldconfig

# for HDDL

WORKDIR /tmp

# hadolint ignore=DL3031, DL3033
RUN yum update -y && yum install -y \
        boost-filesystem \
        boost-thread \
        boost-program-options \
        boost-system \
        boost-chrono \
        boost-date-time \
        boost-regex \
        boost-atomic \
        json-c \
        libXxf86vm-devel && \
    yum clean all && rm -rf /var/cache/yum


# Post-installation cleanup and setting up OpenVINO environment variables
RUN rm -rf /tmp && mkdir /tmp
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

USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers below
