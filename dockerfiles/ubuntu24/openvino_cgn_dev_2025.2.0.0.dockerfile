# Copyright (C) 2019-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:24.04 AS base

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
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino

# Creating user openvino and adding it to groups"users"
RUN useradd -ms /bin/bash -G users openvino

RUN find "${TEMP_DIR}" \( -name "*.tgz" -o -name "*.tar.gz" \) -exec tar -xzf {} \; && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d.\d+')" && \
    OV_YEAR="$(echo "$OV_BUILD" | grep -oP '^[^\d]*(\d+)')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino_"$OV_YEAR" && \
    rm -rf "${TEMP_DIR}" && \
    chown -R openvino /opt/intel/openvino_"$OV_BUILD"


ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/extras/opencv/lib
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino
ENV OV_TOKENIZER_PREBUILD_EXTENSION_PATH=/opt/intel/openvino/runtime/lib/intel64/libopenvino_tokenizers.so
ENV PKG_CONFIG_PATH=/opt/intel/openvino/runtime/lib/intel64/pkgconfig

RUN rm -rf ${INTEL_OPENVINO_DIR}/.distribution && mkdir ${INTEL_OPENVINO_DIR}/.distribution && \
    touch ${INTEL_OPENVINO_DIR}/.distribution/docker
# -----------------



FROM base AS opencv

LABEL description="This is the dev image for OpenCV building with OpenVINO Runtime backend"
LABEL vendor="Intel Corporation"

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        git \
        python3-dev \
        python3-pip \
        python3-venv \
        build-essential \
        cmake \
        ninja-build \
        libgtk-3-dev \
        libpng-dev \
        libjpeg-dev \
        libwebp-dev \
        libtiff5-dev \
        libopenexr-dev \
        libopenblas-dev \
        libx11-dev \
        libavutil-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libswresample-dev \
        # libtbb2 \
        libssl-dev \
        libva-dev \
        libmfx-dev \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev && \
    rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH=$VIRTUAL_ENV/bin:$PATH

# hadolint ignore=DL3013
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir numpy==1.26.4

ARG OPENCV_BRANCH=4.10.0
WORKDIR /opt/repo
RUN git clone https://github.com/opencv/opencv.git
WORKDIR /opt/repo/opencv
RUN git checkout ${OPENCV_BRANCH}
WORKDIR /opt/repo/opencv/build

# hadolint ignore=SC1091
RUN . "${INTEL_OPENVINO_DIR}"/setupvars.sh; \
    cmake -G Ninja \
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
    -D WITH_MFX=ON \
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
    -D VIDEOIO_PLUGIN_LIST=ffmpeg,gstreamer,mfx \
    -D CMAKE_EXE_LINKER_FLAGS=-Wl,--allow-shlib-undefined \
    -D CMAKE_BUILD_TYPE=Release /opt/repo/opencv && \
    ninja -j "$(nproc)" && cmake --install . && \
    rm -Rf install/bin install/etc/samples

WORKDIR /opt/repo/opencv/build/install
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------


FROM ubuntu:24.04 AS ov_base

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 22.04 LTS"
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

COPY --from=base /opt/intel/ /opt/intel/

WORKDIR /thirdparty

ARG INSTALL_SOURCES="no"

ARG DEPS="tzdata \
          curl"

ARG LGPL_DEPS="g++ \
               gcc \
               libc6-dev"
ARG INSTALL_PACKAGES="-c=python -c=core -c=dev"


# hadolint ignore=DL3008
RUN apt-get update && apt-get upgrade -y && \
    dpkg --get-selections | grep -v deinstall | awk '{print $1}' > base_packages.txt  && \
    apt-get install -y --no-install-recommends ${DEPS} && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get reinstall -y ca-certificates && rm -rf /var/lib/apt/lists/* && update-ca-certificates

# hadolint ignore=DL3008, SC2012
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-venv ${LGPL_DEPS} && \
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

RUN curl -L -O  https://github.com/oneapi-src/oneTBB/releases/download/v2021.9.0/oneapi-tbb-2021.9.0-lin.tgz && \
    tar -xzf  oneapi-tbb-2021.9.0-lin.tgz&& \
    cp oneapi-tbb-2021.9.0/lib/intel64/gcc4.8/libtbb.so* /opt/intel/openvino/runtime/lib/intel64/ && \
    rm -Rf oneapi-tbb-2021.9.0*

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
RUN if [ "$INSTALL_SOURCES" = "no" ]; then \
        echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. They are stored in https://storage.openvinotoolkit.org/repositories/openvino/ci_dependencies/container_gpl_sources/." > DockerImage_readme.txt ; \
    fi


ENV InferenceEngine_DIR=/opt/intel/openvino/runtime/cmake
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/extras/opencv/lib
ENV OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/opt/intel/openvino/python:/opt/intel/openvino/python/python3:/opt/intel/openvino/extras/opencv/python
ENV TBB_DIR=/opt/intel/openvino/runtime/3rdparty/tbb/cmake
ENV ngraph_DIR=/opt/intel/openvino/runtime/cmake
ENV OpenVINO_DIR=/opt/intel/openvino/runtime/cmake
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino
ENV OV_TOKENIZER_PREBUILD_EXTENSION_PATH=/opt/intel/openvino/runtime/lib/intel64/libopenvino_tokenizers.so
ENV PKG_CONFIG_PATH=/opt/intel/openvino/runtime/lib/intel64/pkgconfig

# setup python

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH=$VIRTUAL_ENV/bin:$PATH

# hadolint ignore=DL3013
RUN python3 -m pip install  --no-cache-dir --upgrade pip

# dev package
WORKDIR ${INTEL_OPENVINO_DIR}
ARG OPENVINO_WHEELS_VERSION=2025.2.0.0
ARG OPENVINO_WHEELS_URL
# hadolint ignore=SC2102
RUN apt-get update && apt-get install -y --no-install-recommends cmake make git && rm -rf /var/lib/apt/lists/* && \
    if [ -z "$OPENVINO_WHEELS_URL" ]; then \
        python3 -m pip install --no-cache-dir openvino=="${OPENVINO_WHEELS_VERSION}" && \
        python3 -m pip install --no-cache-dir openvino-tokenizers=="${OPENVINO_WHEELS_VERSION}" && \
        python3 -m pip install --no-cache-dir openvino-genai=="${OPENVINO_WHEELS_VERSION}"; \
    else \
        python3 -m pip install --no-cache-dir --pre openvino=="${OPENVINO_WHEELS_VERSION}" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" && \
        python3 -m pip install --no-cache-dir --pre openvino-tokenizers=="${OPENVINO_WHEELS_VERSION}" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" && \
        python3 -m pip install --no-cache-dir --pre openvino-genai=="${OPENVINO_WHEELS_VERSION}" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL"; \
    fi

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
# Please use `third-party-programs-docker-dev.txt` short path to 3d party file if you use the Dockerfile directly from docker_ci/dockerfiles repo folder
COPY dockerfiles/ubuntu24/third-party-programs-docker-dev.txt ${INTEL_OPENVINO_DIR}/licensing
COPY dockerfiles/ubuntu24/third-party-programs-docker-runtime.txt ${INTEL_OPENVINO_DIR}/licensing

COPY --from=opencv /opt/repo/opencv/build/install ${INTEL_OPENVINO_DIR}/extras/opencv
RUN  echo "export OpenCV_DIR=${INTEL_OPENVINO_DIR}/extras/opencv/cmake" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"; \
     echo "export LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/extras/opencv/lib:\$LD_LIBRARY_PATH" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"

# Install dependencies for OV::RemoteTensor
RUN apt-get update && apt-get install -y --no-install-recommends opencl-headers ocl-icd-opencl-dev && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

# build samples into ${INTEL_OPENVINO_DIR}/samples/cpp/samples_bin
WORKDIR ${INTEL_OPENVINO_DIR}/samples/cpp
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
RUN apt-get update && \
    apt-get install -y --no-install-recommends ocl-icd-libopencl1 && \
    apt-get clean ; \
    rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

# GFX driver version 24.48.31907.7
# hadolint ignore=DL3003
RUN mkdir /tmp/gpu_deps && cd /tmp/gpu_deps && \
    curl -L -O https://github.com/intel/intel-graphics-compiler/releases/download/v2.2.3/intel-igc-core-2_2.2.3+18220_amd64.deb && \
    curl -L -O https://github.com/intel/intel-graphics-compiler/releases/download/v2.2.3/intel-igc-opencl-2_2.2.3+18220_amd64.deb && \
    curl -L -O https://github.com/intel/compute-runtime/releases/download/24.48.31907.7/intel-level-zero-gpu-dbgsym_1.6.31907.7_amd64.ddeb && \
    curl -L -O https://github.com/intel/compute-runtime/releases/download/24.48.31907.7/intel-level-zero-gpu_1.6.31907.7_amd64.deb && \
    curl -L -O https://github.com/intel/compute-runtime/releases/download/24.48.31907.7/intel-opencl-icd-dbgsym_24.48.31907.7_amd64.ddeb && \
    curl -L -O https://github.com/intel/compute-runtime/releases/download/24.48.31907.7/intel-opencl-icd_24.48.31907.7_amd64.deb && \
    curl -L -O https://github.com/intel/compute-runtime/releases/download/24.48.31907.7/libigdgmm12_22.5.4_amd64.deb && \
    curl -L -O https://github.com/intel/compute-runtime/releases/download/24.48.31907.7/ww48.sum && \
    sha256sum -c ww48.sum && \
    dpkg -i ./*.deb && rm -Rf /tmp/gpu_deps

# for NPU

# from https://github.com/oneapi-src/level-zero/releases/tag/v1.20.2
# from https://github.com/intel/linux-npu-driver/releases/tag/v1.16.0

# hadolint ignore=DL3003
RUN mkdir /tmp/npu_deps && cd /tmp/npu_deps && \
    curl -L -O https://github.com/oneapi-src/level-zero/releases/download/v1.21.9/level-zero_1.21.9+u24.04_amd64.deb && \
    curl -L -O https://github.com/intel/linux-npu-driver/releases/download/v1.17.0/intel-driver-compiler-npu_1.17.0.20250508-14912879441_ubuntu24.04_amd64.deb && \
    curl -L -O https://github.com/intel/linux-npu-driver/releases/download/v1.17.0/intel-fw-npu_1.17.0.20250508-14912879441_ubuntu24.04_amd64.deb && \
    curl -L -O https://github.com/intel/linux-npu-driver/releases/download/v1.17.0/intel-level-zero-npu_1.17.0.20250508-14912879441_ubuntu24.04_amd64.deb && \
    apt-get update && apt-get install --no-install-recommends -y ./*.deb && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/npu_deps


# Post-installation cleanup and setting up OpenVINO environment variables
ENV LIBVA_DRIVER_NAME=iHD
ENV GST_VAAPI_ALL_DRIVERS=1
ENV LIBVA_DRIVERS_PATH=/usr/lib/x86_64-linux-gnu/dri

RUN apt-get update && \
    apt-get autoremove -y gfortran && \
    rm -rf /var/lib/apt/lists/*

USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}
ENV DEBIAN_FRONTEND=noninteractive

CMD ["/bin/bash"]

# Setup custom layers below
