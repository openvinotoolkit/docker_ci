# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM registry.access.redhat.com/ubi8

LABEL name="rhel8_runtime" \
      maintainer="openvino_docker@intel.com" \
      vendor="Intel Corporation" \
      version="2021.4" \
      release="2021.4" \
      summary="Provides the latest release of Intel(R) Distribution of OpenVINO(TM) toolkit." \
      description="This is the runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on RHEL UBI 8"

USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# get product from URL
ARG package_url=https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4/l_openvino_toolkit_runtime_rhel8_p_2021.4.582.tgz
ARG TEMP_DIR=/tmp/openvino_installer

WORKDIR ${TEMP_DIR}

# install product by copying archive content
ENV INTEL_OPENVINO_DIR /opt/intel/openvino

RUN curl -OL ${package_url} && \
    tar -xzf "${TEMP_DIR}"/*.tgz && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d+')" && \
    OV_YEAR="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino_"$OV_YEAR" && \
    rm -rf ${INTEL_OPENVINO_DIR}/deployment_tools/tools/workbench && rm -rf ${TEMP_DIR}


RUN rm -rf ${INTEL_OPENVINO_DIR}/.distribution && mkdir ${INTEL_OPENVINO_DIR}/.distribution && \
    touch ${INTEL_OPENVINO_DIR}/.distribution/docker

# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino

ARG LGPL_DEPS="gcc-c++"
ARG INSTALL_PACKAGES="-c=opencv_req -c=python -c=opencv_opt"

ARG INSTALL_SOURCES="no"

WORKDIR /thirdparty
# hadolint ignore=DL3031, DL3033, SC2012
RUN yum -y update && rpm -qa --qf "%{name}\n" > base_packages.txt && \
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

# setup Python
ENV PYTHON_VER python3.6

RUN ${PYTHON_VER} -m pip install --upgrade pip

# runtime package

# download source for PyPi LGPL packages
WORKDIR /thirdparty
RUN if [ "$INSTALL_SOURCES" = "yes" ]; then \
        curl -L https://files.pythonhosted.org/packages/81/41/e6cb9026374771e3bdb4c0fe8ac0c51c693a14b4f72f26275da15f7a4d8b/ethtool-0.14.tar.gz --output ethtool-0.14.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/ef/86/c5a34243a932346c59cb25eb49a4d1dec227974209eb9b618d0ed57ea5be/gpg-1.10.0.tar.gz --output gpg-1.10.0.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/e0/e8/1e4f21800015a9ca153969e85fc29f7962f8f82fc5dbc1ecbdeb9dc54c75/PyGObject-3.28.3.tar.gz --output PyGObject-3.28.3.tar.gz; \
    fi

WORKDIR /tmp

RUN ${PYTHON_VER} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/python/${PYTHON_VER}/requirements.txt

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN curl -L https://raw.githubusercontent.com/openvinotoolkit/docker_ci/master/dockerfiles/rhel8/third-party-programs-docker-runtime.txt --output third-party-programs-docker-runtime.txt

# for CPU

# for GPU
ARG INTEL_OPENCL=19.41.14441

RUN groupmod -g 44 video

# hadolint ignore=DL3031, DL3033
WORKDIR ${INTEL_OPENVINO_DIR}/install_dependencies
RUN ./install_NEO_OCL_driver.sh --no_numa -y -d ${INTEL_OPENCL} && \
    yum clean all && rm -rf /var/cache/yum && \
    yum remove -y epel-release


# Post-installation cleanup and setting up OpenVINO environment variables

RUN rm -rf /tmp && mkdir /tmp

RUN if [ -f "${INTEL_OPENVINO_DIR}"/bin/setupvars.sh ]; then \
        printf "\nexport TBB_DIR=\${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/tbb/cmake\n" >> ${INTEL_OPENVINO_DIR}/bin/setupvars.sh; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /home/openvino/.bashrc; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /root/.bashrc; \
    fi;

USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers below
