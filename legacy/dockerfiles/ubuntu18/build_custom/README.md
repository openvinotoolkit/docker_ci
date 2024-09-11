# Build custom Intel® Distribution of OpenVINO™ toolkit Docker image
This repository folder contains the Dockerfile to build a docker image with the Intel® Distribution of OpenVINO™ toolkit.  

## Components
* [OpenVINO™ Toolkit - Deep Learning Deployment Toolkit repository](https://github.com/openvinotoolkit/openvino)
* [OpenCV: Open Source Computer Vision Library](https://github.com/opencv/opencv)
* [OpenVINO™ Toolkit - Open Model Zoo repository](https://github.com/openvinotoolkit/open_model_zoo)

## How to build
Go to the folder with the Dockerfile and run:
```
docker build -t [image:tag] .
```

* `/opt/intel/openvino` folder will contain OpenVINO build
* `/opt/intel/repo` will contain OpenVINO™ and OpenCV git repositories in `openvino` and `opencv` folders accordingly.


If you want to rebuild the entire image, use the docker `--no-cache` option:
```
docker build --no-cache -t image:tag .
```

You can use the docker `--build-arg` option to override the following variables:  
* `OPENVINO_FORK` - To specify a GitHub fork of the OpenVINO repository to use. By default, it is main OpenVINO repository.  
* `OPENVINO_BRANCH`, `OPENCV_BRANCH`, `OMZ_BRANCH` - To specify branches with source code. By default, they are equal to "master".  
* `BUILD_OPENCV_CONTRIB` - If set to `yes`, OpenCV will be built with extra modules (default is `no`). You can use the `OPENCV_CONTRIB_BRANCH` argument to specify a branch in the `opencv_contrib` repository.

**For example**:  
This command builds an image with OpenVINO™ 2021.2 release.
```
docker build -t openvino:2021.2 --build-arg OPENVINO_BRANCH="releases/2021/2" .
```

You can manually set up CMake parameters to build a custom package from source code using these files:  
* [openvino_cmake.txt](openvino_cmake.txt)
* [opencv_cmake.txt](opencv_cmake.txt)

>**Note**:  
By default, these files already contain some parameters for *Debug* build  
Do not override PATH/PREFIX options. This can break a build of package.

### Build stages
The docker image is built using a multi-step build:
1. **setup_openvino**  
    Clone OpenVINO™ git repository with submodules and install build dependencies.  
    Open Model Zoo will be included as a submodule of OpenVINO.
2. **build_openvino**  
    Build OpenVINO™ (CPU, iGPU, VPU support) with the parameters specified in openvino_cmake.txt.  
    It does not include OpenCV.  
3. **copy_openvino**  
    Copy OpenVINO™ build to clear Ubuntu:18.04 image.
4. **openvino**  
    Install OpenVINO™ dependencies. Now you can use it.
5. **opencv**  
    Build and setup OpenCV with the parameters specified in opencv_cmake.txt.  
    OpenCV can be optionally built with extra modules (see the `BUILD_OPENCV_CONTRIB` argument description above).
6. **openvino_repo**  
    Copy OpenVINO source code repository, build artifacts, and Open Model Zoo demos from the `build_openvino` stage.   
    *Note: this stage significantly increases the image size.*

Use the docker `--target` option to specify a final stage.
```
docker build --target [stage] -t [image:tag] .
```

**For example**:  
This command builds an image without OpenCV and OpenVINO source code:
```
docker build --target openvino -t ie:latest .
```

## How to test
You can use our default pipeline to test your image:
```
python3 docker_openvino.py test -t [image:tag] -dist custom 
```

>**Note**:  
Docker CI framework automatically runs the corresponding tests.  
By default, the product version is equal to the latest release version. Use `-p` to override this.

## How to run
Please follow the [Run built image](../get-started.md#run-built-image) section in Docker CI getting started guide.

## Prebuilt images

Prebuilt images are available on: 
- [Docker Hub](https://hub.docker.com/u/openvino)
- [Red Hat* Quay.io](https://quay.io/organization/openvino)
- [Red Hat* Ecosystem Catalog (runtime image)](https://catalog.redhat.com/software/containers/intel/openvino-runtime/606ff4d7ecb5241699188fb3)
- [Red Hat* Ecosystem Catalog (development image)](https://catalog.redhat.com/software/containers/intel/openvino-dev/613a450dc9bc35f21dc4a1f7)
- [Azure* Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/intel_corporation.openvino)


## License
This Dockerfile contains third-party components with different licenses.  
If you are distributing the container as a whole, then you are responsible for license compliance for all of the software it contains.

## Documentation
* [Install Intel® Distribution of OpenVINO™ toolkit for Linux* from a Docker* Image](https://docs.openvino.ai/latest/openvino_docs_install_guides_installing_openvino_docker_linux.html)
* [Install Intel® Distribution of OpenVINO™ toolkit for Windows* from Docker* Image](https://docs.openvino.ai/latest/openvino_docs_install_guides_installing_openvino_docker_windows.html)
* [Official Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
---
\* Other names and brands may be claimed as the property of others.