# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM registry.access.redhat.com/ubi8:8.4

LABEL name="rhel8_runtime" \
      maintainer="openvino_docker@intel.com" \
      vendor="Intel Corporation" \
      version="2022.1.0" \
      release="2022.1.0" \
      summary="Provides the latest release of Intel(R) Distribution of OpenVINO(TM) toolkit." \
      description="This is the runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on RHEL UBI 8"
# hadolint ignore=DL3002
USER root

COPY entitlement.pem /etc/pki/entitlement
COPY entitlement-key.pem /etc/pki/entitlement
COPY ./rhsm-conf /etc/rhsm
COPY ./rhsm-ca /etc/rhsm/ca

WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]




# get product from URL
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer


COPY ${package_url} ${TEMP_DIR}/


# install product by copying archive content

ARG TEMP_DIR=/tmp/openvino_installer
ENV INTEL_OPENVINO_DIR /opt/intel/openvino


WORKDIR ${TEMP_DIR}

RUN tar -xzf "${TEMP_DIR}"/*.tgz && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d.\d+')" && \
    OV_YEAR="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino_"$OV_YEAR" && \
    rm -rf ${INTEL_OPENVINO_DIR}/tools/workbench && rm -rf ${TEMP_DIR}


ENV HDDL_INSTALL_DIR=/opt/intel/openvino/runtime/3rdparty/hddl
ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/extras/opencv/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/3rdparty/hddl/lib
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python/python3.6:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake

RUN rm -rf ${INTEL_OPENVINO_DIR}/.distribution && mkdir ${INTEL_OPENVINO_DIR}/.distribution && \
    touch ${INTEL_OPENVINO_DIR}/.distribution/docker



# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN sed -ri -e 's@^UMASK[[:space:]]+[[:digit:]]+@UMASK 000@g' /etc/login.defs && \
	grep -E "^UMASK" /etc/login.defs && useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino




ARG LGPL_DEPS="gcc-c++"
ARG INSTALL_PACKAGES="-c=opencv_req -c=python -c=opencv_opt"

ARG INSTALL_SOURCES="no"

WORKDIR /thirdparty
# hadolint ignore=DL3031, DL3033, SC2012
RUN rm /etc/rhsm-host && yum update -y --excludepkgs redhat-release && rpm -qa --qf "%{name}\n" > base_packages.txt && \
	yum install -y ${LGPL_DEPS} && \
	${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh -y $INSTALL_PACKAGES && \
	if [ "$INSTALL_SOURCES" = "yes" ]; then \
	    yum install -y yum-utils && \
		rpm -qa --qf "%{name}\n" > all_packages.txt && \
		grep -v -f base_packages.txt all_packages.txt | while read line; do \
		package=$(echo $line); \
		rpm -qa $package --qf "%{name}: %{license}\n" | grep GPL; \
		exit_status=$?; \
		if [ $exit_status -eq 0 ]; then \
		    yumdownloader --skip-broken --source -y $package;  \
		fi \
	  done && \
	  yum autoremove -y yum-utils && \
      echo "Download source for $(ls | wc -l) third-party packages: $(du -sh)"; fi && \
	yum clean all && rm -rf /var/cache/yum

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN if [ "$INSTALL_SOURCES" = "no" ]; then \
        echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. Please use tag <YYYY.U_src> to pull the image with downloaded sources." > DockerImage_readme.txt ; \
    fi

WORKDIR /licenses
RUN cp -rf "${INTEL_OPENVINO_DIR}"/licensing /licenses


ENV HDDL_INSTALL_DIR=/opt/intel/openvino/runtime/3rdparty/hddl
ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/extras/opencv/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/3rdparty/hddl/lib
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python/python3.6:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake

# setup Python
ENV PYTHON_VER python3.6

RUN ${PYTHON_VER} -m pip install --upgrade pip

# runtime package
WORKDIR ${INTEL_OPENVINO_DIR}
ARG OPENVINO_WHEELS_VERSION=2022.1.0
ARG OPENVINO_WHEELS_URL
RUN ${PYTHON_VER} -m pip install --no-cache-dir cmake && \
    if [ -z "$OPENVINO_WHEELS_URL" ]; then \
        ${PYTHON_VER} -m pip install --no-cache-dir openvino=="$OPENVINO_WHEELS_VERSION" ; \
    else \
        ${PYTHON_VER} -m pip install --no-cache-dir --pre openvino=="$OPENVINO_WHEELS_VERSION" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" ; \
    fi

# download source for PyPi LGPL packages
WORKDIR /thirdparty
RUN if [ "$INSTALL_SOURCES" = "yes" ]; then \
        curl -L https://files.pythonhosted.org/packages/81/41/e6cb9026374771e3bdb4c0fe8ac0c51c693a14b4f72f26275da15f7a4d8b/ethtool-0.14.tar.gz --output ethtool-0.14.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/ef/86/c5a34243a932346c59cb25eb49a4d1dec227974209eb9b618d0ed57ea5be/gpg-1.10.0.tar.gz --output gpg-1.10.0.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/e0/e8/1e4f21800015a9ca153969e85fc29f7962f8f82fc5dbc1ecbdeb9dc54c75/PyGObject-3.28.3.tar.gz --output PyGObject-3.28.3.tar.gz; \
    fi

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN curl -L https://raw.githubusercontent.com/openvinotoolkit/docker_ci/releases/2022/1/dockerfiles/rhel8/third-party-programs-docker-runtime.txt --output third-party-programs-docker-runtime.txt

# for CPU

# for GPU
RUN groupmod -g 44 video

# hadolint ignore=DL3031, DL3033
WORKDIR ${INTEL_OPENVINO_DIR}/install_dependencies
RUN ./install_NEO_OCL_driver.sh --no_numa -y && \
    yum clean all && rm -rf /var/cache/yum && \
    yum remove -y epel-release


# Post-installation cleanup and setting up OpenVINO environment variables

RUN rm -rf /tmp && mkdir /tmp && rm -rf /etc/pki/entitlement && rm -rf /etc/rhsm


USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers below
