# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM registry.access.redhat.com/ubi8:8.9 AS base
# hadolint ignore=DL3002
USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]


# get product from URL
ARG package_url=https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.2/linux/l_openvino_toolkit_rhel8_2024.2.0.15519.5c0f38f83f6_x86_64.tgz
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
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/extras/opencv/lib
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



FROM base as opencv  
LABEL description="This is the dev image for OpenCV building with OpenVINO Runtime backend"
LABEL vendor="Intel Corporation"


COPY ./entitlement /etc/pki/entitlement
COPY ./rhsm-conf /etc/rhsm
COPY ./rhsm-ca /etc/rhsm/ca


RUN rm -f /etc/rhsm-host && subscription-manager repos --enable codeready-builder-for-rhel-8-x86_64-rpms
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm && dnf clean all
RUN dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm && dnf clean all
# hadolint ignore=DL3033
RUN yum install -y \
    gtk3-devel \
    gstreamer1-devel \
    gstreamer1-plugins-base-devel \
    ffmpeg-devel \
    libmfx-devel \
    cmake \
    git \
    python38-devel \
    python38-pip \
    gcc-c++  \
    gcc && yum clean all

RUN rm -rf /etc/pki/entitlement && rm -rf /etc/rhsm

RUN python3 -m pip install --no-cache-dir numpy==1.23.1
# 4.8 with a fix for building tests
ARG OPENCV_BRANCH="377be68d923e40900ac5526242bcf221e3f355e5"
WORKDIR /opt/repo
RUN git clone https://github.com/opencv/opencv.git
WORKDIR /opt/repo/opencv
RUN git checkout ${OPENCV_BRANCH}
WORKDIR /opt/repo/opencv/build

# hadolint ignore=SC2046
RUN . "${INTEL_OPENVINO_DIR}"/setupvars.sh; \
    cmake \
    -D BUILD_INFO_SKIP_EXTRA_MODULES=ON \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_JASPER=OFF \
    -D BUILD_JAVA=OFF \
    -D BUILD_JPEG=ON \
    -D BUILD_APPS_LIST=version \
    -D BUILD_opencv_apps=ON \
    -D BUILD_opencv_java=OFF \
    -D BUILD_OPENEXR=OFF \
    -D BUILD_PNG=ON \
    -D BUILD_TBB=OFF \
    -D BUILD_WEBP=OFF \
    -D BUILD_ZLIB=ON \
    -D BUILD_TESTS=ON \
    -D WITH_1394=OFF \
    -D WITH_CUDA=OFF \
    -D WITH_EIGEN=OFF \
    -D WITH_GPHOTO2=OFF \
    -D WITH_GSTREAMER=ON \
    -D OPENCV_GAPI_GSTREAMER=OFF \
    -D WITH_GTK_2_X=OFF \
    -D WITH_IPP=ON \
    -D WITH_JASPER=OFF \
    -D WITH_LAPACK=OFF \
    -D WITH_MATLAB=OFF \
    -D WITH_MFX=OFF \
    -D WITH_OPENCLAMDBLAS=OFF \
    -D WITH_OPENCLAMDFFT=OFF \
    -D WITH_OPENEXR=OFF \
    -D WITH_OPENJPEG=OFF \
    -D WITH_QUIRC=OFF \
    -D WITH_TBB=OFF \
    -D WITH_TIFF=OFF \
    -D WITH_VTK=OFF \
    -D WITH_WEBP=OFF \
    -D CMAKE_USE_RELATIVE_PATHS=ON \
    -D CMAKE_SKIP_INSTALL_RPATH=ON \
    -D ENABLE_BUILD_HARDENING=ON \
    -D ENABLE_CONFIG_VERIFICATION=ON \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D ENABLE_CXX11=ON \
    -D INSTALL_PDB=ON \
    -D INSTALL_TESTS=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D CMAKE_INSTALL_PREFIX=install \
    -D OPENCV_SKIP_PKGCONFIG_GENERATION=ON \
    -D OPENCV_SKIP_PYTHON_LOADER=OFF \
    -D OPENCV_SKIP_CMAKE_ROOT_CONFIG=ON \
    -D OPENCV_GENERATE_SETUPVARS=OFF \
    -D OPENCV_BIN_INSTALL_PATH=bin \
    -D OPENCV_INCLUDE_INSTALL_PATH=include \
    -D OPENCV_LIB_INSTALL_PATH=lib \
    -D OPENCV_CONFIG_INSTALL_PATH=cmake \
    -D OPENCV_3P_LIB_INSTALL_PATH=3rdparty \
    -D OPENCV_SAMPLES_SRC_INSTALL_PATH=samples \
    -D OPENCV_DOC_INSTALL_PATH=doc \
    -D OPENCV_OTHER_INSTALL_PATH=etc \
    -D OPENCV_LICENSES_INSTALL_PATH=etc/licenses \
    -D OPENCV_INSTALL_FFMPEG_DOWNLOAD_SCRIPT=ON \
    -D BUILD_opencv_world=OFF \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D BUILD_opencv_dnn=OFF \
    -D BUILD_opencv_gapi=OFF \
    -D PYTHON3_PACKAGES_PATH=install/python/python3 \
    -D PYTHON3_LIMITED_API=ON \
    -D HIGHGUI_PLUGIN_LIST=all \
    -D OPENCV_PYTHON_INSTALL_PATH=python \
    -D CPU_BASELINE=SSE4_2 \
    -D OPENCV_IPP_GAUSSIAN_BLUR=ON \
    -D WITH_INF_ENGINE=ON \
    -D InferenceEngine_DIR="${INTEL_OPENVINO_DIR}"/runtime/cmake/ \
    -D ngraph_DIR="${INTEL_OPENVINO_DIR}"/runtime/cmake/ \
    -D INF_ENGINE_RELEASE=2022010000 \
    -D VIDEOIO_PLUGIN_LIST=ffmpeg,gstreamer \
    -D CMAKE_EXE_LINKER_FLAGS=-Wl,--allow-shlib-undefined \
    -D CMAKE_BUILD_TYPE=Release /opt/repo/opencv && \
    make -j$(nproc) && cmake -P cmake_install.cmake && \
    rm -Rf install/bin install/etc/samples

WORKDIR /opt/repo/opencv/build/install
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------




# -----------------
FROM registry.access.redhat.com/ubi8:8.9 AS ov_base

LABEL name="rhel8_dev" \
      maintainer="openvino_docker@intel.com" \
      vendor="Intel Corporation" \
      version="2024.2.0" \
      release="2024.2.0" \
      summary="Provides the latest release of Intel(R) Distribution of OpenVINO(TM) toolkit." \
      description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on RHEL UBI 8"

WORKDIR /
USER root

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]



# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN sed -ri -e 's@^UMASK[[:space:]]+[[:digit:]]+@UMASK 000@g' /etc/login.defs && \
	grep -E "^UMASK" /etc/login.defs && useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino



ENV INTEL_OPENVINO_DIR /opt/intel/openvino

COPY --from=base /opt/intel /opt/intel



ARG LGPL_DEPS="gcc-c++ \
               glibc \
               libstdc++ \
               libgcc"
ARG INSTALL_PACKAGES="-c=opencv_req -c=python -c=opencv_opt -c=core -c=dev"

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
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/extras/opencv/lib
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

# dev package
WORKDIR ${INTEL_OPENVINO_DIR}
ARG OPENVINO_WHEELS_VERSION=2024.2.0
ARG OPENVINO_WHEELS_URL
# hadolint ignore=SC2102,DL3033
RUN yum install -y cmake git && yum clean all && \
    if [ -z "$OPENVINO_WHEELS_URL" ]; then \
        ${PYTHON_VER} -m pip install --no-cache-dir openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]=="$OPENVINO_WHEELS_VERSION" --extra-index-url https://download.pytorch.org/whl/cpu; \
    else \
        ${PYTHON_VER} -m pip install --no-cache-dir --pre openvino=="$OPENVINO_WHEELS_VERSION" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" && \
        ${PYTHON_VER} -m pip install --no-cache-dir --pre openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]=="$OPENVINO_WHEELS_VERSION" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" --extra-index-url https://download.pytorch.org/whl/cpu ; \
    fi

# download source for PyPi LGPL packages
WORKDIR /thirdparty
RUN if [ "$INSTALL_SOURCES" = "yes" ]; then \
        curl -L https://files.pythonhosted.org/packages/ee/2d/9cdc2b527e127b4c9db64b86647d567985940ac3698eeabc7ffaccb4ea61/chardet-4.0.0.tar.gz --output chardet-4.0.0.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/81/41/e6cb9026374771e3bdb4c0fe8ac0c51c693a14b4f72f26275da15f7a4d8b/ethtool-0.14.tar.gz --output ethtool-0.14.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/ef/86/c5a34243a932346c59cb25eb49a4d1dec227974209eb9b618d0ed57ea5be/gpg-1.10.0.tar.gz --output gpg-1.10.0.tar.gz; \
        curl -L https://files.pythonhosted.org/packages/e0/e8/1e4f21800015a9ca153969e85fc29f7962f8f82fc5dbc1ecbdeb9dc54c75/PyGObject-3.28.3.tar.gz --output PyGObject-3.28.3.tar.gz; \
    fi

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN curl -L https://raw.githubusercontent.com/openvinotoolkit/docker_ci/master/dockerfiles/rhel8/third-party-programs-docker-runtime.txt --output third-party-programs-docker-runtime.txt && \
    curl -L https://raw.githubusercontent.com/openvinotoolkit/docker_ci/master/dockerfiles/rhel8/third-party-programs-docker-dev.txt --output third-party-programs-docker-dev.txt

COPY --from=opencv /opt/repo/opencv/build/install ${INTEL_OPENVINO_DIR}/extras/opencv
RUN  echo "export OpenCV_DIR=${INTEL_OPENVINO_DIR}/extras/opencv/cmake" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"; \
     echo "export LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/extras/opencv/lib:\$LD_LIBRARY_PATH" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"

# Install dependencies needed by OV::RemoteTensor
RUN yum install -y \
    https://vault.centos.org/centos/8/PowerTools/x86_64/os/Packages/opencl-headers-2.2-1.20180306gite986688.el8.noarch.rpm \
    https://vault.centos.org/centos/8/PowerTools/x86_64/os/Packages/ocl-icd-devel-2.2.12-1.el8.x86_64.rpm \
    https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/ocl-icd-2.2.12-1.el8.x86_64.rpm && \
    yum clean all

# build samples into ${INTEL_OPENVINO_DIR}/samples/cpp/samples_bin
WORKDIR "${INTEL_OPENVINO_DIR}"/samples/cpp
RUN ./build_samples.sh -b /tmp/build -i ${INTEL_OPENVINO_DIR}/samples/cpp/samples_bin && \
    rm -Rf /tmp/build

# add Model API package
# hadolint ignore=DL3013
RUN git clone https://github.com/openvinotoolkit/open_model_zoo && \
    sed -i '/opencv-python/d' open_model_zoo/demos/common/python/requirements.txt && \
    pip3 --no-cache-dir install open_model_zoo/demos/common/python/ && \
    rm -Rf open_model_zoo && \
    python3 -c "from model_zoo import model_api"

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
