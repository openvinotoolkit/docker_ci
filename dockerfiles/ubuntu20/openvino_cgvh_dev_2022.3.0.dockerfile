# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM ubuntu:20.04 AS base

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
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/extras/opencv/lib
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
        libavresample-dev \
        libtbb2 \
        libssl-dev \
        libva-dev \
        libmfx-dev \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir numpy==1.23.1

ARG OPENCV_BRANCH="4.6.0"

WORKDIR /opt/repo
RUN git clone https://github.com/opencv/opencv.git --depth 1 -b ${OPENCV_BRANCH} 
WORKDIR /opt/repo/opencv
RUN git fetch origin 4.x:4.x && \
    git cherry-pick -n 1b1bbe426277715a876878890a3dc88231b871bc

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
    -D INSTALL_C_EXAMPLES=ON \
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
    ninja && cmake --install . && \
    rm -Rf install/bin install/etc/samples

WORKDIR /opt/repo/opencv/build/install
CMD ["/bin/bash"]
# -------------------------------------------------------------------------------------------------


FROM ubuntu:20.04 AS ov_base

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 20.04 LTS"
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
ARG INSTALL_PACKAGES="-c=opencv_req -c=python -c=cl_compiler -c=core -c=dev"


# hadolint ignore=DL3008
RUN apt-get update && \
    dpkg --get-selections | grep -v deinstall | awk '{print $1}' > base_packages.txt  && \
    apt-get install -y --no-install-recommends ${DEPS} && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get reinstall -y ca-certificates && rm -rf /var/lib/apt/lists/* && update-ca-certificates
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
ENV LD_LIBRARY_PATH=/opt/intel/openvino/runtime/3rdparty/hddl/lib:/opt/intel/openvino/runtime/3rdparty/tbb/lib:/opt/intel/openvino/runtime/lib/intel64:/opt/intel/openvino/tools/compile_tool:/opt/intel/openvino/extras/opencv/lib
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

RUN ${PYTHON_VER} -m pip install --upgrade pip

# dev package
WORKDIR ${INTEL_OPENVINO_DIR}
ARG OPENVINO_WHEELS_VERSION=2022.3.0
ARG OPENVINO_WHEELS_URL
# hadolint ignore=SC2102
RUN apt-get update && apt-get install -y --no-install-recommends cmake make git && rm -rf /var/lib/apt/lists/* && \
    if [ -z "$OPENVINO_WHEELS_URL" ]; then \
        ${PYTHON_VER} -m pip install --no-cache-dir openvino=="$OPENVINO_WHEELS_VERSION" && \
        ${PYTHON_VER} -m pip install --no-cache-dir openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]=="$OPENVINO_WHEELS_VERSION" --extra-index-url https://download.pytorch.org/whl/cpu; \
    else \
        ${PYTHON_VER} -m pip install --no-cache-dir --pre openvino=="$OPENVINO_WHEELS_VERSION" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" && \
        ${PYTHON_VER} -m pip install --no-cache-dir --pre openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]=="$OPENVINO_WHEELS_VERSION" --trusted-host=* --find-links "$OPENVINO_WHEELS_URL" --extra-index-url https://download.pytorch.org/whl/cpu; \
    fi

WORKDIR ${INTEL_OPENVINO_DIR}/licensing
# Please use `third-party-programs-docker-dev.txt` short path to 3d party file if you use the Dockerfile directly from docker_ci/dockerfiles repo folder
COPY dockerfiles/ubuntu20/third-party-programs-docker-dev.txt ${INTEL_OPENVINO_DIR}/licensing
COPY dockerfiles/ubuntu20/third-party-programs-docker-runtime.txt ${INTEL_OPENVINO_DIR}/licensing

COPY --from=opencv /opt/repo/opencv/build/install ${INTEL_OPENVINO_DIR}/extras/opencv
RUN  echo "export OpenCV_DIR=${INTEL_OPENVINO_DIR}/extras/opencv/cmake" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"; \
     echo "export LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/extras/opencv/lib:\$LD_LIBRARY_PATH" | tee -a "${INTEL_OPENVINO_DIR}/extras/opencv/setupvars.sh"

# build samples into ${INTEL_OPENVINO_DIR}/samples/cpp/samples_bin
WORKDIR ${INTEL_OPENVINO_DIR}/samples/cpp
RUN ./build_samples.sh -b build && \
    cp -R build/intel64/Release samples_bin && cp build/intel64/Release/libformat_reader.so . && \
    rm -Rf build && mkdir -p build/intel64/Release/lib && mv libformat_reader.so build/intel64/Release/lib/ && rm -Rf samples_bin/lib/

# add Model API package
# hadolint ignore=DL3013
RUN git clone https://github.com/openvinotoolkit/open_model_zoo && \
    sed -i '/opencv-python/d' open_model_zoo/demos/common/python/requirements.txt && \
    pip3 --no-cache-dir install open_model_zoo/demos/common/python/ && \
    rm -Rf open_model_zoo && \
    python3 -c "from openvino.model_zoo import model_api"

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

WORKDIR /opt/libusb-1.0.22/libusb
RUN /bin/mkdir -p '/usr/local/lib' && \
    /bin/bash ../libtool   --mode=install /usr/bin/install -c   libusb-1.0.la '/usr/local/lib' && \
    /bin/mkdir -p '/usr/local/include/libusb-1.0' && \
    /usr/bin/install -c -m 644 libusb.h '/usr/local/include/libusb-1.0' && \
    /bin/mkdir -p '/usr/local/lib/pkgconfig'

WORKDIR /opt/libusb-1.0.22/
RUN /usr/bin/install -c -m 644 libusb-1.0.pc '/usr/local/lib/pkgconfig' && \
    cp ${INTEL_OPENVINO_DIR}/install_dependencies/97-myriad-usbboot.rules /etc/udev/rules.d/ && \
    ldconfig

# for HDDL
WORKDIR /tmp
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libboost-filesystem-dev \
        libboost-program-options-dev \
        libboost-thread-dev \
        libjson-c4 \
        libxxf86vm-dev && \
    rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*


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
