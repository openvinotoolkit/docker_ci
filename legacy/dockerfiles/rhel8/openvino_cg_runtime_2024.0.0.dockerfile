# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM registry.access.redhat.com/ubi8:8.9 AS base
# hadolint ignore=DL3002
USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]


# get product from URL
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer


WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}


# install product by copying archive content

# Creating user openvino and adding it to groups"users"
RUN useradd -ms /bin/bash -G users openvino


ARG TEMP_DIR=/tmp/openvino_installer
ENV INTEL_OPENVINO_DIR /opt/intel/openvino


RUN tar -xzf "${TEMP_DIR}"/*.tgz && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d.\d+')" && \
    OV_YEAR="$(echo "$OV_BUILD" | grep -oP '^[^\d]*(\d+)')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino_"$OV_YEAR" && \
    rm -rf "${INTEL_OPENVINO_DIR}/tools/workbench" && rm -rf "${TEMP_DIR}" && \
    chown -R openvino /opt/intel/openvino_"$OV_BUILD"


ENV HDDL_INSTALL_DIR=/opt/intel/openvino/runtime/3rdparty/hddl
ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino
ENV PKG_CONFIG_PATH=/opt/intel/openvino/runtime/lib/intel64/pkgconfig

RUN rm -rf ${INTEL_OPENVINO_DIR}/.distribution && mkdir ${INTEL_OPENVINO_DIR}/.distribution && \
    touch ${INTEL_OPENVINO_DIR}/.distribution/docker
# -----------------




# -----------------
FROM registry.access.redhat.com/ubi8:8.9 AS ov_base

LABEL name="rhel8_runtime" \
      maintainer="openvino_docker@intel.com" \
      vendor="Intel Corporation" \
      version="2024.0.0" \
      release="2024.0.0" \
      summary="Provides the latest release of Intel(R) Distribution of OpenVINO(TM) toolkit." \
      description="This is the runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on RHEL UBI 8"

WORKDIR /
USER root

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]



# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN sed -ri -e 's@^UMASK[[:space:]]+[[:digit:]]+@UMASK 000@g' /etc/login.defs && \
	grep -E "^UMASK" /etc/login.defs && useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino



ENV INTEL_OPENVINO_DIR /opt/intel/openvino

COPY --from=base /opt/intel /opt/intel



ARG LGPL_DEPS="bash" # no new packages
ARG INSTALL_PACKAGES="-c=python -c=core"

ARG INSTALL_SOURCES="no"

# hadolint ignore=SC2016
RUN sed -i -e 's|https://vault.centos.org/centos/8/PowerTools/$arch/os/Packages/gflags-devel-2.1.2-6|http://mirror.centos.org/centos/8-stream/PowerTools/$arch/os/Packages/gflags-devel-2.2.2-1|g' ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh && \
    sed -i -e 's|https://vault.centos.org/centos/8/PowerTools/$arch/os/Packages/gflags-2.1.2-6|http://mirror.centos.org/centos/8-stream/PowerTools/$arch/os/Packages/gflags-2.2.2-1|g' ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh

WORKDIR /thirdparty
# hadolint ignore=DL3031, DL3033, SC2012
RUN rpm -qa --qf "%{name}\n" > base_packages.txt && \
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


RUN  rm -Rf /etc/pki/entitlement /etc/rhsm/ca /etc/rhsm/rhsm.conf


WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN if [ "$INSTALL_SOURCES" = "no" ]; then \
        echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. They are stored in https://storage.openvinotoolkit.org/repositories/openvino/ci_dependencies/container_gpl_sources/." > DockerImage_readme.txt ; \
    fi

WORKDIR /licenses
RUN cp -rf "${INTEL_OPENVINO_DIR}"/licensing /licenses


ENV HDDL_INSTALL_DIR=/opt/intel/openvino/runtime/3rdparty/hddl
ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino
ENV PKG_CONFIG_PATH=/opt/intel/openvino/runtime/lib/intel64/pkgconfig

# setup Python
ENV PYTHON_VER python3.8

RUN ${PYTHON_VER} -m pip install --upgrade pip

# Install OpenVINO python API dependency
RUN ${PYTHON_VER} -m pip install --no-cache-dir numpy==1.24.4

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN curl -L https://raw.githubusercontent.com/openvinotoolkit/docker_ci/master/dockerfiles/rhel8/third-party-programs-docker-runtime.txt --output third-party-programs-docker-runtime.txt

# for CPU

# for GPU
RUN groupmod -g 44 video
# hadolint ignore=DL3041
RUN dnf install -y libedit ; \
    rpm -ivh https://repositories.intel.com/graphics/rhel/8.6/intel-gmmlib-22.3.1-i529.el8.x86_64.rpm ; \
    rpm -ivh https://repositories.intel.com/graphics/rhel/8.6/intel-igc-core-1.0.12504.6-i537.el8.x86_64.rpm ; \
    rpm -ivh https://repositories.intel.com/graphics/rhel/8.6/intel-igc-opencl-1.0.12504.6-i537.el8.x86_64.rpm ; \
    rpm -ivh https://repositories.intel.com/graphics/rhel/8.6/intel-opencl-22.43.24595.35-i538.el8.x86_64.rpm ; \
    rpm -ivh https://repositories.intel.com/graphics/rhel/8.6/intel-level-zero-gpu-1.3.24595.35-i538.el8.x86_64.rpm ; \
    rpm -ivh https://repositories.intel.com/graphics/rhel/8.6/level-zero-1.8.8-i524.el8.x86_64.rpm ; \
    rpm -ivh http://mirror.centos.org/centos/8-stream/AppStream/x86_64/os/Packages/ocl-icd-2.2.12-1.el8.x86_64.rpm ; \
    dnf clean all


# Post-installation cleanup and setting up OpenVINO environment variables

RUN rm -rf /tmp && mkdir /tmp 


USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers below
