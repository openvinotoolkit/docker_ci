FROM ubuntu:18.04 AS ov_base

LABEL Description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Ubuntu 18.04 LTS"
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
    apt-get install -y --no-install-recommends python3-pip python3-dev lib${PYTHON}=3.6.9-1~18.04 && \
    rm -rf /var/lib/apt/lists/*

# get product from URL
ARG package_url
ARG TEMP_DIR=/tmp/openvino_installer

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}

# install product by installation script
ENV INTEL_OPENVINO_DIR /opt/intel/openvino

RUN tar -xzf ${TEMP_DIR}/*.tgz --strip 1
RUN sed -i 's/decline/accept/g' silent.cfg && \
    ${TEMP_DIR}/install.sh -s silent.cfg && \
    ${INTEL_OPENVINO_DIR}/install_dependencies/install_openvino_dependencies.sh && \
    cp ${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/97-myriad-usbboot.rules /etc/udev/rules.d/ && \
    ldconfig

WORKDIR /tmp
RUN rm -rf ${TEMP_DIR}



# dev package
WORKDIR /tmp

RUN ${PYTHON} -m pip install --no-cache-dir setuptools && \
    find "${INTEL_OPENVINO_DIR}/" -type f -name "*requirements*.*" -path "*/${PYTHON}/*" -exec ${PYTHON} -m pip install --no-cache-dir -r "{}" \; && \
    find "${INTEL_OPENVINO_DIR}/" -type f -name "*requirements*.*" -not -path "*/post_training_optimization_toolkit/*" -not -name "*windows.txt"  -not -name "*ubuntu16.txt" -not -path "*/python3*/*" -not -path "*/python2*/*" -exec ${PYTHON} -m pip install --no-cache-dir -r "{}" \;

WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker
RUN source ${INTEL_OPENVINO_DIR}/bin/setupvars.sh && \
    ${PYTHON} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/requirements.in && \
    ${PYTHON} ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker/setup.py install

WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit
RUN if [ -f requirements.txt ]; then \
        ${PYTHON} -m pip install --no-cache-dir -r ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/requirements.txt && \
        ${PYTHON} ${INTEL_OPENVINO_DIR}/deployment_tools/tools/post_training_optimization_toolkit/setup.py install; \
    fi;


# Post-installation cleanup and setting up OpenVINO environment variables
RUN if [ -f "${INTEL_OPENVINO_DIR}"/bin/setupvars.sh ]; then \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /home/openvino/.bashrc; \
        printf "\nsource \${INTEL_OPENVINO_DIR}/bin/setupvars.sh\n" >> /root/.bashrc; \
    fi;
RUN find "${INTEL_OPENVINO_DIR}/" -name "*.*sh" -type f -exec dos2unix {} \;

USER openvino
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["/bin/bash"]

# Setup custom layers
