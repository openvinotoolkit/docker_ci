# Configuration Guide for the Intel® Graphics Compute Runtime for OpenCL™ on Ubuntu* 20.04

Intel® Graphics Compute Runtime for OpenCL™ driver components are required to use a GPU plugin and write custom layers for Intel® Integrated Graphics.
The driver is installed in the OpenVINO™ Docker image but you need to activate it in the container for a non-root user if you have Ubuntu 20.04 on your host.
To access GPU capabilities, you need to have correct permissions on the host and Docker container.
Run the following commands to list the group assigned ownership of the render nodes on your host:

```bash
$ stat -c "group_name=%G group_id=%g" /dev/dri/render*
group_name=render group_id=134
```

OpenVINO™ Docker images do not contain a render group for openvino non-root user because the render group does not have a strict group ID, unlike the video group.
Choose one of the options below to set up access to GPU device from a container.

## 1. Configure a Host Non-Root User to Use a GPU Device from a OpenVINO Container on Ubuntu 20 Host [RECOMMENDED]

To run an OpenVINO container with default non-root user (openvino) with access to a GPU device, you need to have non-root user with the same id like `openvino` user inside container:
By deafult `openvino` user has #1000 user ID.
Create a non-root user (for e.g. host_openvino) on the host with the same user ID and access to video, render, docker groups:

```bash
$ useradd -u 1000 -G users,video,render,docker host_openvino
```

Now you can use OpenVINO container with GPU access under the non-root user.

```bash
$ docker run -it --rm --device /dev/dri  <image_name>
```

## 2. Configure a Container to Use a GPU Device on Ubuntu 20 Host Under a Non-Root User

To run an OpenVINO container as non-root with access to a GPU device, specify the render group ID from your host:

```bash
$ docker run -it --rm --device /dev/dri  --group-add=<render_group_id_on_host> <image_name> 
```

For example, get the render group ID on your host:

```bash
$ docker run -it --rm --device /dev/dri --group-add=$(stat -c "%g" /dev/dri/render*) <image_name> 
```

Now you can use the container with GPU access under the non-root user.

## 3. Configure an Image to Use a GPU Device on Ubuntu 20 Host and Save It

To run an OpenVINO container as root with access to a GPU device, use the command below:

```bash
$ docker run -it --rm --user root --device /dev/dri --name my_container <image_name>
```

Check groups for the GPU device in the container:

```bash
$ ls -l /dev/dri/
```

The output should look like the following:

```bash
crw-rw---- 1 root video  226,   0 Feb 20 14:28 card0
crw-rw---- 1 root   134  226, 128 Feb 20 14:28 renderD128
```

Create a render group in the container with the same group ID as on your host:

```bash
$ addgroup --gid 134 render
```

Check groups for the GPU device in the container:

```bash
$ ls -l /dev/dri/
```

The output should look like the following:

```bash
crw-rw---- 1 root video  226,   0 Feb 20 14:28 card0
crw-rw---- 1 root render 226, 128 Feb 20 14:28 renderD128
```

Add the non-root user to the render group:

```bash
$ usermod -a -G render openvino
$ id openvino
```

Check that the group now contains the user:

```bash
uid=1000(openvino) gid=1000(openvino) groups=1000(openvino),44(video),100(users),134(render)
```

Then relogin as the non-root user:

```bash
$ su openvino
```

Now you can use the container with GPU access under the non-root user or you can save that container as an image and push it to your registry.
Open another terminal and run the commands below:

```bash
$ docker commit my_container my_image
$ docker run -it --rm --device /dev/dri --user openvino  my_image
```

---
\* Other names and brands may be claimed as the property of others.
