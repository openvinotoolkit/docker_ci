# escape=`
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM mcr.microsoft.com/windows/servercore:ltsc2019 AS ov_base

LABEL Description="This is the data_dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Windows Server LTSC 2019"
LABEL Vendor="Intel Corporation"

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

USER ContainerAdministrator

# setup MSBuild 2019
RUN powershell.exe -Command Invoke-WebRequest -URI https://aka.ms/vs/16/release/vs_buildtools.exe -OutFile %TMP%\\vs_buildtools.exe

RUN %TMP%\\vs_buildtools.exe --quiet --norestart --wait --nocache `
	 --installPath "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools" `
     --add Microsoft.VisualStudio.Workload.MSBuildTools `
     --add Microsoft.VisualStudio.Workload.UniversalBuildTools `
     --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended `
     --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 `
     --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 `
     --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 `
     --remove Microsoft.VisualStudio.Component.Windows81SDK || IF "%ERRORLEVEL%"=="3010" EXIT 0 && powershell set-executionpolicy remotesigned

# setup CMake

RUN powershell.exe -Command `
    Invoke-WebRequest -URI https://cmake.org/files/v3.14/cmake-3.14.7-win64-x64.msi -OutFile %TMP%\\cmake-3.14.7-win64-x64.msi ; `
    Start-Process %TMP%\\cmake-3.14.7-win64-x64.msi -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item %TMP%\\cmake-3.14.7-win64-x64.msi -Force

RUN SETX /M PATH "C:\Program Files\CMake\Bin;%PATH%"

# Setup Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.27.29016

RUN powershell.exe -Command `
    Invoke-WebRequest -URI https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile "%TMP%\vc_redist.x64.exe" ; `
    Start-Process %TMP%\\vc_redist.x64.exe -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item "%TMP%\vc_redist.x64.exe" -Force


# setup Python
ARG PYTHON_VER=python3.7


RUN powershell.exe -Command `
  Invoke-WebRequest -URI https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe -OutFile %TMP%\\python-3.7.exe ; `
  Start-Process %TMP%\\python-3.7.exe -ArgumentList '/passive InstallAllUsers=1 PrependPath=1 TargetDir=c:\\Python37' -Wait ; `
  Remove-Item %TMP%\\python-3.7.exe -Force

RUN python -m pip install --upgrade pip

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
    Expand-Archive -Path "./*.zip" -DestinationPath "%INTEL_OPENVINO_DIR%" -Force ; `
    Remove-Item "./*.zip" -Force

RUN powershell.exe -Command if ( -not (Test-Path -Path C:\intel\openvino) ) `
                    {`
                        New-Item -Path C:\intel\openvino -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%`
                    }`
                    if ( -not (Test-Path -Path C:\intel\openvino_2021) ) `
                    {`
                        New-Item -Path C:\intel\openvino_2021 -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%`
                    }`
                    if (Test-Path -Path %INTEL_OPENVINO_DIR%\deployment_tools\inference_engine)`
                    {`
                        New-Item -Path %INTEL_OPENVINO_DIR%\inference_engine -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%\deployment_tools\inference_engine`
                    }`
                    if (Test-Path -Path %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\models\intel)`
                    {`
                        New-Item -Path %INTEL_OPENVINO_DIR%\deployment_tools\intel_models -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\models\intel ;`
                        New-Item -Path %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\intel_models -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\models\intel`
                    }`
                    if (Test-Path -Path %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\tools\downloader)`
                    {`
                        New-Item -Path %INTEL_OPENVINO_DIR%\deployment_tools\tools\model_downloader -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\tools\downloader`
                    }`
                    if (Test-Path -Path %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\demos)`
                    {`
                        New-Item -Path %INTEL_OPENVINO_DIR%\deployment_tools\inference_engine\demos -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\demos`
                    }`
                    if (Test-Path -Path %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo)`
                    {`
                        New-Item -Path %INTEL_OPENVINO_DIR%\deployment_tools\tools\post_training_optimization_toolkit\libs\open_model_zoo -ItemType SymbolicLink -Value %INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo`
                    }

# for CPU

# data dev package
WORKDIR ${INTEL_OPENVINO_DIR}
RUN python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\python\%PYTHON_VER%\requirements.txt" && `
    python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\python\%PYTHON_VER%\openvino\tools\benchmark\requirements.txt" && `
    python -m pip install --no-cache-dir torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN powershell.exe -Command "Get-ChildItem %INTEL_OPENVINO_DIR% -Recurse -Filter *requirements*.* | ForEach-Object { `
       if (($_.Fullname -like '*post_training_optimization_toolkit*') -or ($_.Fullname -like '*accuracy_checker*') -or ($_.Fullname -like '*python3*') -or ($_.Fullname -like '*python2*') -or ($_.Fullname -like '*requirements_ubuntu*')) `
       {echo 'skipping dependency'} else {echo 'installing dependency'; python -m pip install --no-cache-dir -r $_.FullName} `
   }"

WORKDIR ${INTEL_OPENVINO_DIR}\deployment_tools\open_model_zoo\tools\accuracy_checker
RUN %INTEL_OPENVINO_DIR%\bin\setupvars.bat && `
    python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\tools\accuracy_checker\requirements.in" && `
    python "%INTEL_OPENVINO_DIR%\deployment_tools\open_model_zoo\tools\accuracy_checker\setup.py" install

WORKDIR ${INTEL_OPENVINO_DIR}\deployment_tools\tools\post_training_optimization_toolkit
RUN python -m pip install --no-cache-dir -r "%INTEL_OPENVINO_DIR%\deployment_tools\tools\post_training_optimization_toolkit\requirements.txt" && `
    python "%INTEL_OPENVINO_DIR%\deployment_tools\tools\post_training_optimization_toolkit\setup.py" install


WORKDIR ${INTEL_OPENVINO_DIR}

# Post-installation cleanup
RUN powershell Remove-Item -Force -Recurse "%TEMP%\*" && `
    powershell Remove-Item -Force -Recurse "%TEMP_DIR%" && `
    rmdir /S /Q "%ProgramData%\Package Cache"

USER ContainerUser

CMD ["cmd.exe"]

# Setup custom layers below
