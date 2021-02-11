# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:18.04 AS base

# hadolint ignore=DL3002
USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends curl tzdata ca-certificates && \
    rm -rf /var/lib/apt/lists/*


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

ARG INSTALL_SOURCES="no"


ARG DEPS="dpkg-dev \
          tzdata \
          curl"

ARG LGPL_DEPS="g++ \
               gcc \
               libc6-dev"
ARG INSTALL_PACKAGES="-c=opencv_req -c=python -c=opencv_opt -c=dlstreamer -c=cl_compiler"



# hadolint ignore=DL3008
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ${DEPS} && \
    dpkg --get-selections | grep -v deinstall | awk '{print $1}' > base_packages.txt  && \
    rm -rf /var/lib/apt/lists/*


# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends ${LGPL_DEPS} && \
    ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh -y ${INSTALL_PACKAGES} && \
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
    rm -rf /var/lib/apt/lists/* && rm -rf *.txt


WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN if [ "$INSTALL_SOURCES" = "no" ]; then \
        echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. Please use tag <YYYY.U_src> to pull the image with downloaded sources." > DockerImage_readme.txt ; \
    fi


# setup Python
ENV PYTHON_VER python3.6



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
    find "${INTEL_OPENVINO_DIR}/deployment_tools/model_optimizer/" -type f \( -name "*requirements*.txt" -and -not -name "*requirements_tf.txt" \) -print -exec ${PYTHON_VER} -m pip install --no-cache-dir -r "{}" \; && \
    find "${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/downloader/" -type f -name "*requirements*.in" -print -exec ${PYTHON_VER} -m pip install --no-cache-dir -r "{}" \; && \
    deactivate


WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker
RUN source ${INTEL_OPENVINO_DIR}/bin/setupvars.sh && \
    ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/requirements.in && \
    ${PYTHON_VER} ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/setup.py install && \
    rm -rf ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/build

# download source for PyPi LGPL packages
WORKDIR /thirdparty
RUN if [ "$INSTALL_SOURCES" = "yes" ]; then \
        curl -L https://files.pythonhosted.org/packages/7f/e6/1639d2de28c27632e3136015ecfd67774cca6f55146507baeaef06b113ba/pypi-kenlm-0.1.20190403.tar.gz --output pypi-kenlm.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/ee/2d/9cdc2b527e127b4c9db64b86647d567985940ac3698eeabc7ffaccb4ea61/chardet-4.0.0.tar.gz --output chardet-4.0.0.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/81/47/5f2cea0164e77dd40726d83b4c865c2a701f60b73cb6af7b539cd42aafb4/flake8-import-order-0.18.1.tar.gz --output lake8-import-order-0.18.1.tar.gz; \
    fi

WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit
RUN ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/requirements.txt && \
    ${PYTHON_VER} ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/setup.py install && \
    rm -rf ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/build

# for CPU

# for GPU
ARG INTEL_OPENCL
ARG TEMP_DIR=/tmp/opencl


WORKDIR ${INTEL_OPENVINO_DIR}/install_dependencies
RUN ./install_NEO_OCL_driver.sh --no_numa -y -d ${INTEL_OPENCL} && \
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
    rm -rf /var/lib/apt/lists/* && rm -rf *.txt

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
