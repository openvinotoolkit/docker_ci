# Build custom Intel® Distribution of OpenVINO™ toolkit Docker image
This repository folder contains Dockerfile to build a docker image with the Intel® Distribution of OpenVINO™ toolkit.  

## Components
* [OpenVINO™ Toolkit - Deep Learning Deployment Toolkit repository](https://github.com/openvinotoolkit/openvino)
* [OpenCV: Open Source Computer Vision Library](https://github.com/opencv/opencv)
* [OpenVINO™ Toolkit - Open Model Zoo repository](https://github.com/openvinotoolkit/open_model_zoo)

## How to build
Go to the folder with the Dockerfile and run:
```
docker build -t [image:tag] .
```

If you want to rebuild the entire image, use docker `--no-cache` option:
```
docker build --no-cache -t image:tag .
```

You can use docker `--build-arg` option to override the following variables:  
`OPENVINO_BRANCH`, `OPENCV_BRANCH`, `OMZ_BRANCH` - To specify a branches with source code. By default, they are equal to "master".  
`OCL_VERSION` - To specify the version of Intel® Graphics Compute Runtime for OpenCL™ Driver on Linux. By default, it is equal to "19.41.14441".

**For example**:  
This command builds an image with OpenVINO™ 2021.2 release.
```
docker build -t openvino:2021.2 --build-arg OPENVINO_BRANCH="releases/2021/2" .
```

You can manually setup cmake parameters to build a custom package from source code using these files:  
* [openvino_cmake.txt](openvino_cmake.txt)
* [opencv_cmake.txt](opencv_cmake.txt)

>**Note**:  
By default, these files already contain some parameters.  
Do not override PATH/PREFIX options. This can break a build of package.

### Build stages
The docker image is built using a multi-step build:
1. **setup_openvino**  
    Clone OpenVINO™ git repository with submodules and install build dependencies.
2. **build_openvino**  
    Build OpenVINO™ (CPU, iGPU, VPU support) with the parameters specified in openvino_cmake.txt.  
    It doesn't include OpenCV and Open Model Zoo.
3. **copy_openvino**  
    Copy OpenVINO™ build to clear Ubuntu:18.04 image.
4. **openvino**  
    Install OpenVINO™ dependencies. Now you can use it.
5. **opencv**  
    Build and setup OpenCV with the parameters specified in opencv_cmake.txt.
6. **open_model_zoo**  
    Clone and setup Open Model Zoo repository.

Use docker `--target` option to specify a final stage.
```
docker build --target [stage] -t [image:tag] .
```

**For example**:  
This command builds an image without Open Model Zoo.
```
docker build --target opencv -t ie:opencv .
```

## How to test
You can use our default pipeline to test your image:
```
python3 docker_openvino.py test -t [image:tag] -dist custom 
```

>**Note**:  
Docker_ci automatically runs the corresponding tests.  
By default, the product version is equal to the latest release version. Use `-p` to override this.

## How to run
Please follow [Run built image](../get-started.md#run-built-image) section in DockerHub CI getting started guide.

## Prebuilt images
Prebuilt images are available on [Docker Hub](https://hub.docker.com/u/openvino)

## License
This Dockerfile contains third-party components with different licenses.  
If you are distributing the container as a whole, then you are responsible for license compliance for all of the software it contains.

## Documentation
* [Install Intel® Distribution of OpenVINO™ toolkit for Linux* from a Docker* Image](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_docker_linux.html)
* [Install Intel® Distribution of OpenVINO™ toolkit for Windows* from Docker* Image](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_docker_windows.html)
* [Official Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
---
\* Other names and brands may be claimed as the property of others.