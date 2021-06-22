FROM openvino/ubuntu18_dev_no_samples:2021.4_tgl

ARG db_password
ARG rabbitmq_password
ARG PACKAGE_LINK

ENV DEBIAN_FRONTEND noninteractive
ENV ACCURACY_CHECKER_LOG_LEVEL ERROR

ENV RABBITMQ_PASSWORD $rabbitmq_password
ENV OPENVINO_WORKBENCH_ROOT ${INTEL_OPENVINO_DIR}/deployment_tools/tools/workbench
ENV OPENVINO_WORKBENCH_DATA_PATH ${OPENVINO_WORKBENCH_ROOT}/wb/data
ENV PYTHONPATH ${PYTHONPATH}:${OPENVINO_WORKBENCH_ROOT}:${OPENVINO_WORKBENCH_ROOT}/wb/main/console_tool_wrapper/winograd_tool/winograd_cli_tool:${INTEL_OPENVINO_DIR}/deployment_tools/tools/benchmark_tool:${OPENVINO_WORKBENCH_ROOT}/model_analyzer:${INTEL_OPENVINO_DIR}/deployment_tools/tools/benchmark_tool

ENV PYTHON_VERSION 3.6
ENV PYTHON python${PYTHON_VERSION}

ENV USER_NAME workbench
ENV USER_ID 5665
ENV GROUP_NAME ${USER_NAME}
ENV GROUP_ID ${USER_ID}

ENV DB_PASSWORD $db_password
ENV DB_USER ${USER_NAME}
ENV DB_NAME workbench

USER root

RUN groupadd -g ${GROUP_ID} ${GROUP_NAME}
RUN useradd ${USER_NAME} -u ${USER_ID} -g ${GROUP_ID} -ms /bin/bash  && \
    chown ${USER_NAME} -R /home/${USER_NAME}

ENV WORKBENCH_PUBLIC_DIR /home/${USER_NAME}/.workbench
ENV WORKBENCH_POSTGRESQL_DATA_DIR ${WORKBENCH_PUBLIC_DIR}/postgresql_data_directory
ENV JUPYTER_BASE_DIR /home/${USER_NAME}/.jupyter
ENV JUPYTER_USER_SETTINGS_DIR ${JUPYTER_BASE_DIR}/lab/user-settings

ENV DEPENDENCIES " \
    postgresql \
    rabbitmq-server \
    nginx \
    gettext-base \
    unzip \
    dpkg-dev \
"

RUN sed -Ei 's/# deb-src /deb-src /' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends ${DEPENDENCIES} && \
    apt-get source gettext-base && \
    apt-get remove -y dpkg-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN ${PYTHON} -m pip install pip==19.3.1

WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/tools
RUN rm -rf ${OPENVINO_WORKBENCH_ROOT}
ADD --chown=workbench workbench ${OPENVINO_WORKBENCH_ROOT}/

# COPY JUPYTER TUTORIALS TO WORKBENCH PUBLIC ARTIFACTS DIRECTORY
COPY --chown=workbench workbench/tutorials ${WORKBENCH_PUBLIC_DIR}/tutorials

# COPY JUPYTER USER SETTINGS
COPY --chown=workbench workbench/docker/jupyter_config/user-settings ${JUPYTER_USER_SETTINGS_DIR}

# SET PERMISSIONS FOR DIRECTORIES
RUN find ${WORKBENCH_PUBLIC_DIR} -type d -exec chmod 777 {} \;


# SET OWNERSHIP FOR WORKBENCH PUBLIC ARTIFACTS DIRECTORY
RUN chown -R ${USER_NAME} ${WORKBENCH_PUBLIC_DIR}

# SET UP DEPENDENCIES FOR SERVER
RUN mkdir -m 777 -p ${OPENVINO_WORKBENCH_DATA_PATH} && chown -R ${USER_NAME} ${OPENVINO_WORKBENCH_ROOT}

RUN ${PYTHON} -m pip install --no-cache-dir -r ${OPENVINO_WORKBENCH_ROOT}/requirements/requirements.txt && \
    ${PYTHON} -m pip install --no-cache-dir -r ${OPENVINO_WORKBENCH_ROOT}/requirements/requirements_jupyter.txt && \
    ${PYTHON} -m pip install --no-cache-dir -r ${OPENVINO_WORKBENCH_ROOT}/model_analyzer/requirements.txt

RUN chown -R ${USER_NAME}:${GROUP_NAME} ${JUPYTER_BASE_DIR}

RUN xargs -n 1 curl -O < ${OPENVINO_WORKBENCH_ROOT}/docker/docker_python_lgpl.txt

# Add ${USER_NAME} user to groups nginx, postgres and rabbitmq for running
# services without sudo
RUN for g in $(id -nG postgres); do gpasswd -a ${USER_NAME} ${g}; done && \
    for g in $(id -nG rabbitmq); do gpasswd -a ${USER_NAME} ${g}; done && \
    gpasswd -a ${USER_NAME} users && \
    gpasswd -a ${USER_NAME} video && \
    gpasswd -a ${USER_NAME} adm

RUN touch /var/run/nginx.pid && \
    rm -rf /etc/nginx/sites-enabled/default && \
    cp  ${OPENVINO_WORKBENCH_ROOT}/nginx/nginx.conf /etc/nginx/nginx.conf

RUN chown -R ${USER_NAME} /var/lib/postgresql /var/run/postgresql \
                          /var/lib/rabbitmq /var/log/rabbitmq /var/log/rabbitmq \
                          /var/log/nginx /var/lib/nginx /var/run/nginx.pid /etc/nginx


USER workbench

WORKDIR ${OPENVINO_WORKBENCH_ROOT}

RUN python3.6 ${OPENVINO_WORKBENCH_ROOT}/wb/main/utils/bundle_creator/bundle_downloader.py \
                        --link ${PACKAGE_LINK} \
                        -os ubuntu18 ubuntu20 \
                        --output-path ${OPENVINO_WORKBENCH_ROOT}/bundles \
                        --targets cpu gpu hddl opencv python3.6 python3.7 python3.8 vpu

ENTRYPOINT ["bash", "/opt/intel/openvino/deployment_tools/tools/workbench/docker/scripts/docker-entrypoint.sh"]
