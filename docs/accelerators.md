# Using OpenVINO™ Toolkit containers with GPU accelerators


Containers can be used to execute inference operations with GPU acceleration.

There are the following prerequisites:

- Use the Linux kernel with GPU models supported by you integrated GPU or discrete GPU. Check the documetnation on https://dgpu-docs.intel.com/driver/kernel-driver-types.html. 
On Linux host, confirm if there is available a character device /dev/dri

- On Windows Subsystem for Linux (WSL2) refere to the guidelines on https://docs.openvino.ai/nightly/openvino_docs_install_guides_configurations_for_intel_gpu.html# 
Note, that on WLS2, there muse be present a character device `/dev/drx`.

- Docker image for the container must include GPU runtime drivers like described on https://docs.openvino.ai/nightly/openvino_docs_install_guides_configurations_for_intel_gpu.html# 

While the host and preconfigured and docker engine is up and running, use the following docker parameters while starting the container:

## Linux

The command below should report both CPU and GPU device available for inference execution:
```
export IMAGE=openvino/ubuntu20_dev:2023.0.0
docker run -it --device /dev/dri --group-add=$(stat -c \"%g\" /dev/dri/render* ) $IMAGE ./samples/cpp/samples_bin/hello_query_device
```

`--device /dev/dri` - it passed the GPU device to the container
`--group-add` - it adds a security context to the container command with permisssion to use the GPU device

## Windows Subsystem for Linux

On WSL2, the command starting the container is like below:

```
export IMAGE=openvino/ubuntu20_dev:2023.0.0
docker run -it --device=/dev/dxg -v /usr/lib/wsl:/usr/lib/wsl $IMAGE ./samples/cpp/samples_bin/hello_query_device
```
`--device /dev/dri` - it passed the virtual GPU device to the container
`-v /usr/lib/wsl:/usr/lib/wsl` - it mount in the container required wsl libs


## Usage example:

Run the benchmark all using GPU accelerator with a OV::RemoteTensor
```
docker run --device /dev/dri --group-add=$(stat -c \"%g\" /dev/dri/render* ) $IMAGE bash -c " \
   curl -O https://storage.openvinotoolkit.org/repositories/open_model_zoo/2022.1/models_bin/3/resnet50-binary-0001/FP32-INT1/resnet50-binary-0001.xml && \
   curl -O https://storage.openvinotoolkit.org/repositories/open_model_zoo/2022.1/models_bin/3/resnet50-binary-0001/FP32-INT1/resnet50-binary-0001.bin && \
   ./samples/cpp/samples_bin/benchmark_app -m resnet50-binary-0001.xml -d GPU -use_device_mem -inference_only=false"
```
In the benchmark app, the parameter `-use_device_mem` employs the OV::RemoteTensor as the input buffer. It demonstrates the gain without data copy beteen the host and the GPU device.












