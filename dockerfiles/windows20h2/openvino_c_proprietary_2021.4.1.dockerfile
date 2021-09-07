# escape=`
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM mcr.microsoft.com/windows:20H2 AS ov_base

LABEL description="This is the proprietary image for Intel(R) Distribution of OpenVINO(TM) toolkit on Windows OS 20H2"
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

# install product by installation script
ARG build_id
ENV INTEL_OPENVINO_DIR C:\intel

RUN powershell.exe -Command `
    Start-Process "./*.exe" -ArgumentList '--s --a install --eula=accept --installdir=%INTEL_OPENVINO_DIR% --output=%TMP%\openvino_install_out.log --components=OPENVINO_COMMON,INFERENCE_ENGINE,INFERENCE_ENGINE_SDK,INFERENCE_ENGINE_SAMPLES,OMZ_TOOLS,POT,INFERENCE_ENGINE_CPU,INFERENCE_ENGINE_GPU,MODEL_OPTIMIZER,OMZ_DEV,OPENCV_PYTHON,OPENCV_RUNTIME,OPENCV,DOCS,SETUPVARS,VC_REDIST_2017_X64,icl_redist' -Wait

ENV INTEL_OPENVINO_DIR C:\intel\openvino_${build_id}

RUN powershell.exe -Command if ( -not (Test-Path -Path C:\intel\openvino) ) `
                    {`
                        New-Item -Path C:\intel\openvino -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%`
                    }

# Post-installation cleanup
RUN rmdir /S /Q "%USERPROFILE%\Downloads\Intel"

# for CPU

# proprietary package
WORKDIR ${INTEL_OPENVINO_DIR}

RUN python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\python\%PYTHON_VER%\requirements.txt" && `
    python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\python\%PYTHON_VER%\openvino\tools\benchmark\requirements.txt"


RUN powershell.exe -Command "Get-ChildItem %INTEL_OPENVINO_DIR% -Recurse -Filter *requirements*.* | ForEach-Object { `
       if (($_.Fullname -like '*post_training_optimization_toolkit*') -or ($_.Fullname -like '*accuracy_checker*') -or ($_.Fullname -like '*python3*') -or ($_.Fullname -like '*python2*') -or ($_.Fullname -like '*requirements_ubuntu*')) `
       {echo 'skipping dependency'} else {echo 'installing dependency'; python -m pip install --no-cache-dir -r $_.FullName} `
   }"


# download source for LGPL packages

RUN powershell.exe -Command `
    Invoke-WebRequest -URI https://files.pythonhosted.org/packages/ee/2d/9cdc2b527e127b4c9db64b86647d567985940ac3698eeabc7ffaccb4ea61/chardet-4.0.0.tar.gz -OutFile %INTEL_OPENVINO_DIR%\\deployment_tools\\open_model_zoo\\chardet-4.0.0.tar.gz ; `
    Invoke-WebRequest -URI https://files.pythonhosted.org/packages/81/47/5f2cea0164e77dd40726d83b4c865c2a701f60b73cb6af7b539cd42aafb4/flake8-import-order-0.18.1.tar.gz -OutFile %INTEL_OPENVINO_DIR%\\deployment_tools\\open_model_zoo\\flake8-import-order-0.18.1.tar.gz



WORKDIR ${INTEL_OPENVINO_DIR}\deployment_tools\open_model_zoo\tools\accuracy_checker
RUN %INTEL_OPENVINO_DIR%\bin\setupvars.bat && `
    python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\tools\accuracy_checker\requirements.in" && `
    python -m pip install --no-cache-dir .


WORKDIR ${INTEL_OPENVINO_DIR}\deployment_tools\tools\post_training_optimization_toolkit
RUN python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\deployment_tools\tools\post_training_optimization_toolkit\requirements.txt" && `
    python -m pip install --no-cache-dir .





RUN pip uninstall -y opencv-python



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
