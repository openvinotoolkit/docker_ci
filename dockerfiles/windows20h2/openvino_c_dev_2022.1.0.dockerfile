# escape=`
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM mcr.microsoft.com/windows:20H2 AS ov_base

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Windows OS 20H2"
LABEL vendor="Intel Corporation"

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

USER ContainerAdministrator




# Setup Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.27.29016

RUN powershell.exe -Command `
    Invoke-WebRequest -URI https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile "%TMP%\vc_redist.x64.exe" ; `
    Start-Process %TMP%\\vc_redist.x64.exe -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item "%TMP%\vc_redist.x64.exe" -Force


# setup Python
ARG PYTHON_VER=python3.8


RUN powershell.exe -Command `
  Invoke-WebRequest -URI https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe -OutFile %TMP%\\python-3.8.exe ; `
  Start-Process %TMP%\\python-3.8.exe -ArgumentList '/passive InstallAllUsers=1 PrependPath=1 TargetDir=c:\\Python38' -Wait ; `
  Remove-Item %TMP%\\python-3.8.exe -Force

# hadolint ignore=DL3013
RUN python -m pip install --no-cache-dir --upgrade pip

# download package from external URL
ARG package_url
ARG TEMP_DIR=/temp

WORKDIR ${TEMP_DIR}
# hadolint ignore=DL3020
ADD ${package_url} ${TEMP_DIR}

# install product by copying archive content
ARG build_id
ENV INTEL_OPENVINO_DIR C:\intel\openvino_${build_id}

RUN powershell.exe -Command `
    Expand-Archive -Path "./*.zip" -DestinationPath . -Force ; `
    $OV_FOLDER=(Get-ChildItem -Filter "*openvino*" -Directory).FullName ; `
    New-Item -Path C:\intel\ -ItemType Directory -Name openvino_%build_id% ; `
    Move-Item -Path $OV_FOLDER\* -Destination %INTEL_OPENVINO_DIR% ; `
    Remove-Item @("""./*.zip""",$OV_FOLDER) -Force -Recurse

RUN powershell.exe -Command if ( -not (Test-Path -Path C:\intel\openvino) ) `
                    {`
                        New-Item -Path C:\intel\openvino -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%`
                    }`
                    if ( -not (Test-Path -Path C:\intel\openvino_2022) ) `
                    {`
                        New-Item -Path C:\intel\openvino_2022 -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%`
                    }

# for CPU

# dev package
WORKDIR ${INTEL_OPENVINO_DIR}
ARG OPENVINO_WHEELS_VERSION=2022.1.0
ARG OPENVINO_WHEELS_URL
RUN IF not defined OPENVINO_WHEELS_URL ( `
        python -m pip install --no-cache-dir openvino==%OPENVINO_WHEELS_VERSION% && `
        python -m pip install --no-cache-dir openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]==%OPENVINO_WHEELS_VERSION% --use-deprecated=legacy-resolver `
    ) ELSE ( `
        python -m pip install --no-cache-dir --pre openvino==%OPENVINO_WHEELS_VERSION% --trusted-host=* --find-links %OPENVINO_WHEELS_URL% && `
        python -m pip install --no-cache-dir --pre openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]==%OPENVINO_WHEELS_VERSION% --trusted-host=* --find-links %OPENVINO_WHEELS_URL% `
    )


RUN rmdir /s /q %INTEL_OPENVINO_DIR%\.distribution & mkdir %INTEL_OPENVINO_DIR%\.distribution && `
    copy /b NUL %INTEL_OPENVINO_DIR%\.distribution\docker

WORKDIR ${INTEL_OPENVINO_DIR}

# Post-installation cleanup
RUN powershell Remove-Item -Force -Recurse "%TEMP%\*" && `
    powershell Remove-Item -Force -Recurse "%TEMP_DIR%" && `
    rmdir /S /Q "%ProgramData%\Package Cache"

USER ContainerUser

CMD ["cmd.exe"]

# Setup custom layers below
