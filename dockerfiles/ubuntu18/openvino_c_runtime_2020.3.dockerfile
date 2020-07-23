FROM ubuntu:18.04 AS ov_base

LABEL Description="This is the runtime image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
LABEL Vendor="Intel Corporation"

USER root
WORKDIR /

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Creating user openvino and adding it to groups "video" and "users" to use GPU and VPU
RUN useradd -ms /bin/bash -G video,users openvino && \
    chown openvino -R /home/openvino

ARG DEPENDENCIES="autoconf \
                  automake \
                  build-essential \
                  cmake \
                  cpio \
                  curl \
                  gnupg2 \
                  libdrm2 \
                  libglib2.0-0 \
                  lsb-release \
                  libgtk-3-0 \
                  libtool \
                  udev \
                  unzip \
                  dos2unix"

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /thirdparty
RUN sed -Ei 's/# deb-src /deb-src /' /etc/apt/sources.list && \
    apt-get update && \
    apt-get source ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*


# setup Python
ENV PYTHON python3.6

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip python3-dev lib${PYTHON} && \
    rm -rf /var/lib/apt/lists/*

# get product from local archive
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer

WORKDIR ${TEMP_DIR}
COPY ${package_url} ${TEMP_DIR}

# install product by copying archive content
ARG TEMP_DIR=/tmp/openvino_installer
ENV INTEL_OPENVINO_DIR /opt/intel/openvino

RUN export OV_BUILD OV_FOLDER

RUN tar -xzf "${TEMP_DIR}"/*.tgz && \
    OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.\d+')" && \
    OV_FOLDER="$(find . -maxdepth 1 -type d -name "*openvino*")" && \
    mkdir -p /opt/intel/openvino_"$OV_BUILD"/ && \
    cp -rf "$OV_FOLDER"/*  /opt/intel/openvino_"$OV_BUILD"/ && \
    rm -rf "${TEMP_DIR:?}"/"$OV_FOLDER" && \
    ln --symbolic /opt/intel/openvino_"$OV_BUILD"/ /opt/intel/openvino && \
    ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh && \
    cp ${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/97-myriad-usbboot.rules /etc/udev/rules.d/ && \
    ldconfig

WORKDIR /tmp
RUN rm -rf "${TEMP_DIR}"



# runtime package
WORKDIR /tmp
RUN ${PYTHON} -m pip install --no-cache-dir setuptools && \
    find "${INTEL_OPENVINO_DIR}/" -type f -name "*requirements*.*" -path "*/${PYTHON}/*" -exec ${PYTHON} -m pip install --no-cache-dir -r "{}" \; && \
    find "${INTEL_OPENVINO_DIR}/" -type f -name "*requirements*.*" -not -path "*/post_training_optimization_toolkit/*" -not -name "*windows.txt"  -not -name "*ubuntu16.txt" -not -path "*/python3*/*" -not -path "*/python2*/*" -exec ${PYTHON} -m pip install --no-cache-dir -r "{}" \;


# Post-installation cleanup and setting up OpenVINO environment variables
RUN if [ -f "${INTEL_OPENVINO_DIR}"/bin/setupvars.sh ]; then \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /home/openvino/.bashrc; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /root/.bashrc; \
    fi;
RUN if [ -d "${INTEL_OPENVINO_DIR}"/opt/intel/mediasdk ]; then \
        printf "\nexport LIBVA_DRIVER_NAME=iHD \nexport LIBVA_DRIVERS_PATH=/opt/intel/openvino/opt/intel/mediasdk/lib64/ \nexport GST_VAAPI_ALL_DRIVERS=1 \nexport LIBRARY_PATH=/opt/intel/openvino/opt/intel/mediasdk/lib64/:\$LIBRARY_PATH \nexport LD_LIBRARY_PATH=/opt/intel/openvino/opt/intel/mediasdk/lib64/:\$LD_LIBRARY_PATH \n" >> /home/openvino/.bashrc; \
        printf "\nexport LIBVA_DRIVER_NAME=iHD \nexport LIBVA_DRIVERS_PATH=/opt/intel/openvino/opt/intel/mediasdk/lib64/ \nexport GST_VAAPI_ALL_DRIVERS=1 \nexport LIBRARY_PATH=/opt/intel/openvino/opt/intel/mediasdk/lib64/:\$LIBRARY_PATH \nexport LD_LIBRARY_PATH=/opt/intel/openvino/opt/intel/mediasdk/lib64/:\$LD_LIBRARY_PATH \n" >> /root/.bashrc; \
    fi;
RUN find "${INTEL_OPENVINO_DIR}/" -name "*.*sh" -type f -exec dos2unix {} \;

USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers
