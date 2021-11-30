# Using OpenVINO Docker containers via VS Code

## Introduction

The purpose of this tutorial is to examine [Intel® Distribution of OpenVINO™ toolkit](https://software.intel.com/openvino-toolkit) development containers.

This tutorial will go step-by-step to demonstrate how to set up an OpenVINO™ custom development container under Visual Studio Code* to use it as your full-time development environment.

## Prerequisites

This tutorial requires the following:
 - Installed and run [Docker](https://www.docker.com/products/docker-desktop)* engine/service on the host
 - Install [Visual Studio Code*](https://code.visualstudio.com/)
	- Install the [Remote Development extension pack](https://aka.ms/vscode-remote/download/extension) allows you to open any folder in a container
	- Install the [Remote - Containers extension](https://code.visualstudio.com/docs/remote/containers-tutorial#_install-the-extension) lets you run Visual Studio Code inside a Docker container
 - Clone or download [Docker CI repository](https://github.com/openvinotoolkit/docker_ci) with Dockerfiles
 
## Overview

Intel® Distribution of OpenVINO™ toolkit is produced from different open source and closed source repositories and components. As well OpenVINO has a couple of dependencies which need to be present on your computer. Additionally, to install some of them, you need to have root/admin rights. This might not be desirable. Using Docker and Visual Studio Code integration represents a much cleaner way of development. 

We prepared Dockerfiles for custom development OpenVINO™ from source based on [Ubuntu 18](https://github.com/openvinotoolkit/docker_ci/tree/master/dockerfiles/ubuntu18/build_custom) and [Ubuntu 20](https://github.com/openvinotoolkit/docker_ci/tree/master/dockerfiles/ubuntu20/build_custom). They include the following components:
 
* [OpenVINO™ Toolkit - Deep Learning Deployment Toolkit repository](https://github.com/openvinotoolkit/openvino)
* [OpenCV: Open Source Computer Vision Library](https://github.com/opencv/opencv)
* [OpenVINO™ Toolkit - Open Model Zoo repository](https://github.com/openvinotoolkit/open_model_zoo)

You can customize Cmake* build parameters for OpenVINO itself and OpenCV as well. Then you can integrate that image into VS Code and use all opportunities of the visual code editor and Debug mode for regular development. 

## Docker and VS Code integration

## Build OpenVINO custom development Docker
The first step, we need to build a OpenVINO™ Docker image, by default it uses Debug mode and master branch for all repositories.
Go to the Docker CI repository local copy and run `docker build` from `docker_ci/dockerfiles/<os>/build_custom` folder:

```sh
docker build -t openvino-master .
```

The second step, we need to run it for future usage:

```sh
docker run -it --rm --name openvino openvino-master
```

By default, the container runs under root user.
- `-it` option needs to run container in an interactive mode
- `--rm` option needs to remove container after execution
- `--name` option sets name for container to simplify access to it

Now, we can attach to the container from VS Code. 

## Integrate VS Code and OpenVINO container

Fire up VS Code:

```cmd
code .
```

*Note:* You can use a container on a remote host as well. At first you need connect to the remote host and then execute connection to the container. See [explicit instructions](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host) on VS Code site.

To attach to a Docker container, either select **Remote-Containers: Attach to Running Container...** from the Command Palette (F1) or use the **Remote Explorer** in the Activity Bar and from the Containers view, select the **Attach to Container** inline action on the container you want to connect to.

Then, you can open OpenVINO build and repositories in VS Code editor:

 - Open Explorer -> Open Folder -> `/opt/intel/openvino`
 - Open Explorer -> Open Folder -> `/opt/intel/repo`

You can find OpenVINO samples in `/opt/intel/openvino/deployment_tools/inference_engine/samples` folder, lets try to debug some of them.

## Debug C++ sample

*Prerequisites:* Install [Microsoft C/C++ Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools#:~:text=The%20C%2FC%2B%2B%20extension%20adds,such%20as%20IntelliSense%20and%20debugging.) to VS Code

To build the C++ sample applications for Linux, go to the `/opt/intel/openvino/inference_engine/samples/cpp` directory, respectively, and run the `build_samples.sh` script. By default, it builds C++ samples in Release mode. 

Lets build samples in Debug mode. We need to update `build_samples.sh` script and change _Release_ to _Debug_ on `#60 line "cmake -DCMAKE_BUILD_TYPE=Debug "$SAMPLES_PATH"" ` and run the script.

Then, you can see built samples in `/root/inference_engine_cpp_samples_build/intel64/Debug/` folder.

Select the Run icon in the Activity Bar on the side of VS Code to bring up the [Run view](https://code.visualstudio.com/docs/editor/debugging#_run-view). You can also use the keyboard shortcut `Ctrl+Shift+D`.
If running and debugging is not yet configured (no launch.json has been created), VS Code shows the Run start view. Click on "create a launch.json file" link and select an option "C/C++ (gdb) Launch". 
Please update launch.json with the following settings:

```sh
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "/root/inference_engine_cpp_samples_build/intel64/Debug/hello_query_device",
            "args": [],
            "stopAtEntry": false,
            "cwd": "/root/inference_engine_cpp_samples_build/intel64/Debug/",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
```

After that you can access to the launch.json file via default command palette flow: `View -> Command Palette... (F1) -> Open launch.json`.

Now, you can set a **Breakpoint** on any place of `samples/cpp/hello_query_device/main.cpp` sample and run Debug (F5).

## Debug Python sample

*Prerequisites:* Install [Python extention](https://marketplace.visualstudio.com/items?itemName=ms-python.python) to VS Code

Lets try [Hello Query Device Python* Sample](https://docs.openvinotoolkit.org/latest/openvino_inference_engine_ie_bridges_python_sample_hello_query_device_README.html) which queries Inference Engine devices and prints their metrics and default configuration values.
You need to setup Python interpreter in VS Code: `View -> Command Palette... (F1) -> Python: Select Interpreter` to run Python sample.

Then you need to **Add Configuration** for the Python sample.
Select the Run icon in the Activity Bar on the side of VS Code to bring up the [Run view](https://code.visualstudio.com/docs/editor/debugging#_run-view). You can also use the keyboard shortcut `Ctrl+Shift+D`.
If running and debugging is not yet configured (no launch.json has been created), VS Code shows the Run start view. Click on "create a launch.json file" link and select an option "Python: Current file". 
You will see Debug Configuration with the following settings:

```sh
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
```

After that you can access to the launch.json file via default command palette flow: `View -> Command Palette... (F1) -> Open launch.json`.

Now, you can set a **Breakpoint** on any place of `samples/python/hello_query_device/hello_query_device.py` sample and run Debug (F5).

## Summary

In this article, we briefly introduced the debugging process using OpenVINO custom development container and VS Code editor. Of course, there is much more to try. We hope that this article has motivated you to try it yourself and maybe continue to explore all the possibilities of OpenVINO Docker images.

## References

 - [Available OpenVINO Docker images](https://github.com/openvinotoolkit/docker_ci#prebuilt-images)
 - [Docker CI framework for Intel® Distribution of OpenVINO™ toolkit](https://github.com/openvinotoolkit/docker_ci). The Framework can generate a Dockerfile, build, test, and deploy an image with the Intel® Distribution of OpenVINO™ toolkit. You can reuse available Dockerfiles, add your layer and customize the image of OpenVINO™ for your needs.
 - [VS Code Developing inside a Container article](https://code.visualstudio.com/docs/remote/containers)