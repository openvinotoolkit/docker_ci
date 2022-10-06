# escape=`
# Copyright (C) 2019-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
FROM mcr.microsoft.com/windows/servercore:ltsc2019 AS base

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

USER ContainerAdministrator


ARG HTTPS_PROXY



# setup MSBuild 2019
ARG VS_DIR=/temp/msbuild2019

WORKDIR ${VS_DIR}
COPY scripts\msbuild2019\ ${VS_DIR}
RUN vs_buildtools.exe --quiet --norestart --wait --nocache --noUpdateInstaller --noWeb `
     --add Microsoft.VisualStudio.Workload.MSBuildTools `
     --add Microsoft.VisualStudio.Workload.UniversalBuildTools `
     --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended `
     --channelUri C:\doesntExist.chman && powershell set-executionpolicy remotesigned

# Setup Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.27.29016

RUN powershell.exe -Command `
    $ProgressPreference = 'SilentlyContinue' ; `
    Invoke-WebRequest -URI https://aka.ms/vs/16/release/vc_redist.x64.exe -Proxy %HTTPS_PROXY%  -OutFile "%TMP%\vc_redist.x64.exe" ; `
    Start-Process %TMP%\\vc_redist.x64.exe -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item "%TMP%\vc_redist.x64.exe" -Force



RUN powershell.exe -Command `
        $ProgressPreference = 'SilentlyContinue' ; `
	Invoke-WebRequest -URI https://github.com/python/cpython/archive/refs/tags/v3.8.12.zip -OutFile %TMP%\\python.zip -Proxy %HTTPS_PROXY% ; `
	Expand-Archive -Path %TMP%\\python.zip -DestinationPath c:\\ -Force ; Remove-Item %TMP%\\python.zip -Force ; `
	Invoke-WebRequest -URI https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip -OutFile %TMP%\\python-for-build.zip -Proxy %HTTPS_PROXY% ; `
	Expand-Archive -Path %TMP%\\python-for-build.zip -DestinationPath c:\\python-38-10 -Force ; Remove-Item %TMP%\\python-for-build.zip -Force ; `
    Invoke-WebRequest -URI https://github.com/python/cpython-bin-deps/archive/1cf06233e3ceb49dc0a73c55e04b1174b436b632.zip -OutFile %TMP%\\libffi.zip -Proxy %HTTPS_PROXY% ; `
	Expand-Archive -Path %TMP%\\libffi.zip -DestinationPath c:\\ -Force ; Remove-Item %TMP%\\libffi.zip -Force


RUN C:\cpython-3.8.12\PCbuild\get_externals.bat --python c:\python-38-10\python.exe && `
    rmdir /s /q C:\cpython-3.8.12\externals\libffi && mkdir C:\cpython-3.8.12\externals\libffi && `
    xcopy /s /y c:\cpython-bin-deps-1cf06233e3ceb49dc0a73c55e04b1174b436b632\* c:\cpython-3.8.12\externals\libffi\ && `
    break > C:\cpython-3.8.12\PCbuild\get_externals.bat

RUN C:\cpython-3.8.12\PCbuild\build.bat -p x64


# -----------------
FROM mcr.microsoft.com/windows/servercore:ltsc2019 AS ov_base

LABEL description="This is the dev image for Intel(R) Distribution of OpenVINO(TM) toolkit on Windows Server LTSC 2019"
LABEL vendor="Intel Corporation"

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

USER ContainerAdministrator


ARG HTTPS_PROXY



# setup MSBuild 2019
ARG VS_DIR=/temp/msbuild2019

WORKDIR ${VS_DIR}
COPY scripts\msbuild2019\ ${VS_DIR}
RUN vs_buildtools.exe --quiet --norestart --wait --nocache --noUpdateInstaller --noWeb `
     --add Microsoft.VisualStudio.Workload.MSBuildTools `
     --add Microsoft.VisualStudio.Workload.UniversalBuildTools `
     --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended `
     --channelUri C:\doesntExist.chman && powershell set-executionpolicy remotesigned

# setup CMake



RUN powershell.exe -Command `
    $ProgressPreference = 'SilentlyContinue' ; `
    Invoke-WebRequest -URI https://github.com/Kitware/CMake/releases/download/v3.14.7/cmake-3.14.7-win64-x64.msi -Proxy %HTTPS_PROXY% -OutFile %TMP%\\cmake-3.14.7-win64-x64.msi ; `
    Start-Process %TMP%\\cmake-3.14.7-win64-x64.msi -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item %TMP%\\cmake-3.14.7-win64-x64.msi -Force

RUN SETX /M PATH "C:\Program Files\CMake\Bin;%PATH%"

# Setup Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.27.29016

RUN powershell.exe -Command `
    $ProgressPreference = 'SilentlyContinue' ; `
    Invoke-WebRequest -URI https://aka.ms/vs/16/release/vc_redist.x64.exe -Proxy %HTTPS_PROXY%  -OutFile "%TMP%\vc_redist.x64.exe" ; `
    Start-Process %TMP%\\vc_redist.x64.exe -ArgumentList '/quiet /norestart' -Wait ; `
    Remove-Item "%TMP%\vc_redist.x64.exe" -Force

FROM ov_base

# setup Python
ARG PYTHON_VER=python3.8

COPY --from=base C:\cpython-3.8.12\PCbuild\amd64 c:\Python38
COPY --from=base c:\cpython-3.8.12\Lib c:\Python38\Lib

RUN setx /M path "%path%;C:\Python38;C:\Python38\Scripts"
# hadolint ignore=DL3013
RUN python -m ensurepip --upgrade --default-pip && `
    python -m pip install --no-cache-dir --upgrade pip

# get product from local path
ARG package_url
ARG TEMP_DIR=/temp

WORKDIR ${TEMP_DIR}
COPY ${package_url} ${TEMP_DIR}

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
# hadolint ignore=DL3013
RUN python -m pip uninstall -y opencv-python && `
    python -m pip install --no-cache-dir opencv-python-headless


RUN rmdir /s /q %INTEL_OPENVINO_DIR%\.distribution & mkdir %INTEL_OPENVINO_DIR%\.distribution && `
    copy /b NUL %INTEL_OPENVINO_DIR%\.distribution\docker

WORKDIR ${INTEL_OPENVINO_DIR}

# Install git
RUN cmd /S /C curl -kL --output MinGit.zip https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.1/MinGit-2.35.1-64-bit.zip && powershell -Command Expand-Archive MinGit.zip -DestinationPath c:\\\\MinGit && set PATH="C:\MinGit\cmd\;%PATH%"

RUN setupvars.bat

# Setup vcvars64.bat
WORKDIR C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build
RUN vcvars64.bat
WORKDIR ${INTEL_OPENVINO_DIR}

# Clone OpenCV
RUN c:\\\\MinGit\\\\cmd\\\\git.exe clone --recurse-submodules https://github.com/opencv/opencv.git && mkdir "build-opencv" && cd "build-opencv" && mkdir "install"


RUN cd %INTEL_OPENVINO_DIR% && setupvars.bat && cd "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build" && vcvars64.bat && cd %INTEL_OPENVINO_DIR%\build-opencv && cmake -G Ninja -DBUILD_INFO_SKIP_EXTRA_MODULES=ON -DBUILD_EXAMPLES=OFF -DBUILD_JASPER=OFF -DBUILD_JAVA=OFF -DBUILD_JPEG=ON -DBUILD_APPS_LIST=version -DBUILD_opencv_apps=ON -DBUILD_opencv_java=OFF -DBUILD_OPENEXR=OFF -DBUILD_PNG=ON -DBUILD_TBB=OFF -DBUILD_WEBP=OFF -DBUILD_ZLIB=ON -DWITH_1394=OFF -DWITH_CUDA=OFF -DWITH_EIGEN=OFF -DWITH_GPHOTO2=OFF -DWITH_GSTREAMER=OFF -DOPENCV_GAPI_GSTREAMER=OFF -DWITH_GTK_2_X=OFF -DWITH_IPP=ON -DWITH_JASPER=OFF -DWITH_LAPACK=OFF -DWITH_MATLAB=OFF -DWITH_MFX=OFF -DWITH_OPENCLAMDBLAS=OFF -DWITH_OPENCLAMDFFT=OFF -DWITH_OPENEXR=OFF -DWITH_OPENJPEG=OFF -DWITH_QUIRC=OFF -DWITH_TBB=OFF -DWITH_TIFF=OFF -DWITH_VTK=OFF -DWITH_WEBP=OFF -DCMAKE_USE_RELATIVE_PATHS=ON -DCMAKE_SKIP_INSTALL_RPATH=ON -DENABLE_BUILD_HARDENING=ON -DENABLE_CONFIG_VERIFICATION=ON -DENABLE_PRECOMPILED_HEADERS=OFF -DENABLE_CXX11=ON -DINSTALL_PDB=ON -DINSTALL_TESTS=ON -DINSTALL_C_EXAMPLES=ON -DINSTALL_PYTHON_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=install -DOPENCV_SKIP_PKGCONFIG_GENERATION=ON -DOPENCV_SKIP_PYTHON_LOADER=OFF -DOPENCV_SKIP_CMAKE_ROOT_CONFIG=ON -DOPENCV_GENERATE_SETUPVARS=OFF -DOPENCV_BIN_INSTALL_PATH=bin -DOPENCV_INCLUDE_INSTALL_PATH=include -DOPENCV_LIB_INSTALL_PATH=lib -DOPENCV_CONFIG_INSTALL_PATH=cmake -DOPENCV_3P_LIB_INSTALL_PATH=3rdparty -DOPENCV_SAMPLES_SRC_INSTALL_PATH=samples -DOPENCV_DOC_INSTALL_PATH=doc -DOPENCV_OTHER_INSTALL_PATH=etc -DOPENCV_LICENSES_INSTALL_PATH=etc/licenses -DOPENCV_INSTALL_FFMPEG_DOWNLOAD_SCRIPT=ON -DBUILD_opencv_world=OFF -DBUILD_opencv_python2=OFF -DBUILD_opencv_python3=ON -DPYTHON3_PACKAGES_PATH=install/python/python3 -DPYTHON3_LIMITED_API=ON -DOPENCV_PYTHON_INSTALL_PATH=python -DCPU_BASELINE=SSE4_2 -DOPENCV_IPP_GAUSSIAN_BLUR=ON -DWITH_OPENVINO=ON -DINF_ENGINE_RELEASE=2022020000 -DInferenceEngine_DIR=%INTEL_OPENVINO_DIR%/runtime/cmake -Dngraph_DIR=%INTEL_OPENVINO_DIR%/runtime/cmake/ -DVIDEOIO_PLUGIN_LIST=msmf -DCMAKE_BUILD_TYPE=Release C:\\intel\\openvino\\opencv && ninja && cmake --install . && cmake --build . --target install

RUN setx /M OpenCV_DIR "C:\intel\openvino_2022.2.0.7713\build-opencv\install"
RUN setx /M path "C:\intel\openvino_2022.2.0.7713\build-opencv\install\bin;%path%"
RUN setx /M PYTHONPATH "C:\intel\openvino_2022.2.0.7713\build-opencv\install\python;%PYTHONPATH%"

WORKDIR ${INTEL_OPENVINO_DIR}

# Post-installation cleanup
RUN powershell Remove-Item -Force -Recurse "%TEMP%\*" && `
    powershell Remove-Item -Force -Recurse "%TEMP_DIR%" && `
    rmdir /S /Q "%ProgramData%\Package Cache"

USER ContainerUser

CMD ["cmd.exe"]

# Setup custom layers below
