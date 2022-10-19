# escape=`
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM mcr.microsoft.com/windows:20H2 AS base

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

USER ContainerAdministrator




# setup MSBuild 2019
RUN powershell.exe -Command $ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest -URI https://aka.ms/vs/16/release/vs_buildtools.exe -OutFile %TMP%\\vs_buildtools.exe

RUN %TMP%\\vs_buildtools.exe --quiet --norestart --wait --nocache `
	 --installPath "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools" `
     --add Microsoft.VisualStudio.Workload.MSBuildTools `
     --add Microsoft.VisualStudio.Workload.UniversalBuildTools `
     --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended `
     --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 `
     --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 `
     --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 `
     --remove Microsoft.VisualStudio.Component.Windows81SDK || IF "%ERRORLEVEL%"=="3010" EXIT 0 && powershell set-executionpolicy remotesigned

# Setup Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.27.29016

RUN powershell.exe -Command `
    $ProgressPreference = 'SilentlyContinue' ; `
    Invoke-WebRequest -URI https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile "%TMP%\vc_redist.x64.exe" ; `
    Start-Process %TMP%\\vc_redist.x64.exe -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item "%TMP%\vc_redist.x64.exe" -Force



RUN powershell.exe -Command `
        $ProgressPreference = 'SilentlyContinue' ; `
	Invoke-WebRequest -URI https://github.com/python/cpython/archive/refs/tags/v3.8.12.zip -OutFile %TMP%\\python.zip ; `
	Expand-Archive -Path %TMP%\\python.zip -DestinationPath c:\\ -Force ; Remove-Item %TMP%\\python.zip -Force ; `
	Invoke-WebRequest -URI https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip -OutFile %TMP%\\python-for-build.zip ; `
	Expand-Archive -Path %TMP%\\python-for-build.zip -DestinationPath c:\\python-38-10 -Force ; Remove-Item %TMP%\\python-for-build.zip -Force ; `
    Invoke-WebRequest -URI https://github.com/python/cpython-bin-deps/archive/1cf06233e3ceb49dc0a73c55e04b1174b436b632.zip -OutFile %TMP%\\libffi.zip ; `
	Expand-Archive -Path %TMP%\\libffi.zip -DestinationPath c:\\ -Force ; Remove-Item %TMP%\\libffi.zip -Force


RUN C:\cpython-3.8.12\PCbuild\get_externals.bat --python c:\python-38-10\python.exe && `
    rmdir /s /q C:\cpython-3.8.12\externals\libffi && mkdir C:\cpython-3.8.12\externals\libffi && `
    xcopy /s /y c:\cpython-bin-deps-1cf06233e3ceb49dc0a73c55e04b1174b436b632\* c:\cpython-3.8.12\externals\libffi\ && `
    break > C:\cpython-3.8.12\PCbuild\get_externals.bat

RUN C:\cpython-3.8.12\PCbuild\build.bat -p x64


# -----------------
FROM mcr.microsoft.com/windows:20H2 AS ov_base

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Windows OS 20H2"
LABEL vendor="Intel Corporation"

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

USER ContainerAdministrator




# setup MSBuild 2019
RUN powershell.exe -Command $ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest -URI https://aka.ms/vs/16/release/vs_buildtools.exe -OutFile %TMP%\\vs_buildtools.exe

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
    $ProgressPreference = 'SilentlyContinue' ; `
    Invoke-WebRequest -URI https://github.com/Kitware/CMake/releases/download/v3.14.7/cmake-3.14.7-win64-x64.msi -OutFile %TMP%\\cmake-3.14.7-win64-x64.msi ; `
    Start-Process %TMP%\\cmake-3.14.7-win64-x64.msi -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item %TMP%\\cmake-3.14.7-win64-x64.msi -Force

RUN SETX /M PATH "C:\Program Files\CMake\Bin;%PATH%"

# Setup Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.27.29016

RUN powershell.exe -Command `
    $ProgressPreference = 'SilentlyContinue' ; `
    Invoke-WebRequest -URI https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile "%TMP%\vc_redist.x64.exe" ; `
    Start-Process %TMP%\\vc_redist.x64.exe -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item "%TMP%\vc_redist.x64.exe" -Force


# setup Python
ARG PYTHON_VER=python3.8

COPY --from=base C:\cpython-3.8.12\PCbuild\amd64 c:\Python38
COPY --from=base c:\cpython-3.8.12\Lib c:\Python38\Lib

RUN setx /M path "%path%;C:\Python38;C:\Python38\Scripts"
# hadolint ignore=DL3013
RUN python -m ensurepip --upgrade --default-pip && `
    python -m pip install --no-cache-dir --upgrade pip

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
ARG OPENVINO_WHEELS_VERSION=2022.2.0
ARG OPENVINO_WHEELS_URL
RUN IF not defined OPENVINO_WHEELS_URL ( `
        python -m pip install --no-cache-dir openvino==%OPENVINO_WHEELS_VERSION% && `
        python -m pip install --no-cache-dir openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]==%OPENVINO_WHEELS_VERSION% --use-deprecated=legacy-resolver `
    ) ELSE ( `
        python -m pip install --no-cache-dir --pre openvino==%OPENVINO_WHEELS_VERSION% --trusted-host=* --find-links %OPENVINO_WHEELS_URL% && `
        python -m pip install --no-cache-dir --pre openvino_dev[caffe,kaldi,mxnet,onnx,pytorch,tensorflow2]==%OPENVINO_WHEELS_VERSION% --trusted-host=* --find-links %OPENVINO_WHEELS_URL% `
    )


# install opencv
WORKDIR ${INTEL_OPENVINO_DIR}
RUN cmd /S /C curl -kL --output opencv-4.6.0-vc14_vc15.exe `
    https://github.com/opencv/opencv/releases/download/4.6.0/opencv-4.6.0-vc14_vc15.exe && `
    powershell.exe -Command Start-Process C:\intel\openvino\opencv-4.6.0-vc14_vc15.exe `
    -ArgumentList '-o"C:\\\\intel\\\\openvino\\\\extras\\\\" -y /quiet /norestart' -Wait && `
    del opencv-4.6.0-vc14_vc15.exe
ENV OpenCV_DIR C:\intel\openvino\extras\opencv\build

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
