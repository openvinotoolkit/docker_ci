-# Geting Started with OpenVINO™ Toolkit Images

You can easily get started by using the precompiled and publish docker images.
In order to start using them you need to have the following prerequisites:
- Linux operating system or Windows Subsystem for Linux (WSL2)
- Installed docker engine or compatible container engine
- Permissions to start containers (sudo or docker group membership)

## Pull a docker image

```
docker pull openvino/ubuntu20_dev:latest
```

## Start the container interacctively

```bash
export IMAGE=openvino/ubuntu20_dev:latest
docker run -it --rm $IMAGE
```

Inside the interactive session, you can run all OpenVINO samples and tools.

# Run a python sample
If you want to try some samples, then run the image with the command below:

```bash
docker run -it --rm $IMAGE /bin/bash -c "python3 samples/python/hello_query_device/hello_query_device.py"
```

# Download a model via omz_downloader
```
docker run -it -u $(id -u):$(id -g) -v $(pwd)/:/model/ --rm $IMAGE \
/bin/bash -c "omz_downloader --name googlenet-v1 --precisions FP32 -o /model"
```
# Convert the model to IR format
```
docker run -it -u $(id -u):$(id -g) -v $(pwd)/:/model/ --rm $IMAGE \
/bin/bash -c "omz_converter --name googlenet-v1 --precision FP32 -d /model -o /model"
```
In result the converted model will be copied to `public/googlenet-v1/FP32` folder in the current directly:
```
tree public/googlenet-v1/
public/googlenet-v1/
├── FP32
│   ├── googlenet-v1.bin
│   └── googlenet-v1.xml
├── googlenet-v1.caffemodel
├── googlenet-v1.prototxt
└── googlenet-v1.prototxt.orig
```

# Run a benchmark app

```
docker run -it -u $(id -u):$(id -g) -v $(pwd)/:/model/ --rm $IMAGE benchmark_app -m /model/public/googlenet-v1/FP32/googlenet-v1.xml
```

Check also:

[Working with OpenVINO Containers](docs/containers.md)

[Deployment with GPU accelerator](docs/accelerators.md)

[Generating dockerfiles and building the images in Docker_CI tools](docs/openvino_docker.md)

