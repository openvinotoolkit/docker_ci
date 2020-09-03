FROM mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2019

LABEL Description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Windows Server LTSC 2019"
LABEL Vendor="Intel Corporation"

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

USER ContainerAdministrator




# setup CMake

RUN powershell.exe -Command \
    Invoke-WebRequest -URI https://cmake.org/files/v3.14/cmake-3.14.7-win64-x64.msi -OutFile %TMP%\\cmake-3.14.7-win64-x64.msi ; \
    Start-Process %TMP%\\cmake-3.14.7-win64-x64.msi -ArgumentList '/quiet /norestart' -Wait ; \
    Remove-Item %TMP%\\cmake-3.14.7-win64-x64.msi -Force

RUN SETX /M PATH "C:\Program Files\CMake\Bin;%PATH%"

# setup Python
ARG PYTHON=python3.6


RUN powershell.exe -Command \
  Invoke-WebRequest -URI https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe -OutFile %TMP%\\python-3.6.exe ; \
  Start-Process %TMP%\\python-3.6.exe -ArgumentList '/passive InstallAllUsers=1 PrependPath=1 TargetDir=C:\\Python36' -Wait ; \
  Remove-Item %TMP%\\python-3.6.exe -Force

RUN python -m pip install cmake

# download package from external URL
ARG package_url
ARG TEMP_DIR=/temp

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}

# install product by installation script
ARG build_id
ENV INTEL_OPENVINO_DIR C:/openvino

RUN powershell.exe -Command \
  Start-Process "./*.exe" -ArgumentList '--s --a install --eula=accept --installdir=%INTEL_OPENVINO_DIR% --output=%TMP%/openvino_install_out.log' -Wait; \
  Remove-Item "./*.exe" -Force

ENV INTEL_OPENVINO_DIR C:/openvino/openvino_${build_id}

# for CPU

# dev package
WORKDIR ${INTEL_OPENVINO_DIR}
RUN python -m pip install --no-cache-dir setuptools && \
    python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\python\%PYTHON%\requirements.txt" && \
    python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\python\%PYTHON%\openvino\tools\benchmark\requirements.txt" && \
    python -m pip install --no-cache-dir torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

WORKDIR ${TEMP_DIR}
COPY scripts/install_requirements.bat install_requirements.bat
RUN install_requirements.bat %INTEL_OPENVINO_DIR%

WORKDIR ${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/accuracy_checker
RUN python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\tools\accuracy_checker\requirements.in" && \
    python "%INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\tools\accuracy_checker\setup.py" install


USER ContainerUser

# Post-installation cleanup
WORKDIR ${INTEL_OPENVINO_DIR}

CMD ["cmd.exe"]

# Setup custom layers
