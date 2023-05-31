# Working with OpenVINO™ Toolkit Images

## Runtime images

The runtime images include OpenVINO toolkit with all required dependencies to run inference operations and openvino API both in python and C++.
There are no development tools installed.
Here are examples how to runtime image could be used:

```
export IMAGE=openvino/ubuntu20_runtime:2023.0.0
```

### Building and Using the OpenVINO samples:

```
docker run -it -u root $IMAGE bash -c "/opt/intel/openvino/install_dependencies/install_openvino_dependencies.sh -y -c dev && ./samples/cpp/build_samples.sh && \
/root/openvino_cpp_samples_build/intel64/Release/hello_query_device"
```

### Using python samples
```
docker run -it $IMAGE python3 samples/python/hello_query_device/hello_query_device.py
```

## Development images

Dev images include the OpenVINO runtime components and in addition also development tools. It includes a complete environment for experimenting with OpenVINO.
Below are examples how the development container can be used:

```
export IMAGE=openvino/ubuntu20_dev:2023.0.0
```

### Listing OpenVINO Model Zoo Models
```
docker run $IMAGE omz_downloader --print_all
```

### Download a model
```
mkdir model
docker run -u $(id -u) --rm -v $(pwd)/model:/tmp/model $IMAGE omz_downloader --name mozilla-deepspeech-0.6.1 -o /tmp/model
```

### Convert the model to IR format 
```
docker run -u $(id -u) --rm -v $(pwd)/model:/tmp/model $IMAGE omz_converter --name mozilla-deepspeech-0.6.1 -d /tmp/model -o /tmp/model/converted/
```

### Run benchmark app to test the model performance
```
docker run -u $(id -u) --rm -v $(pwd)/model:/tmp/model $IMAGE benchmark_app -m /tmp/model/converted/public/mozilla-deepspeech-0.6.1/FP32/mozilla-deepspeech-0.6.1.xml
```

### Run a demo from an OpenVINO Model Zoo
```
docker run $IMAGE bash -c "git clone --depth=1 --recurse-submodules --shallow-submodules https://github.com/openvinotoolkit/open_model_zoo.git && \
   cd open_model_zoo/demos/classification_demo/python && \
   curl -O https://storage.openvinotoolkit.org/repositories/open_model_zoo/2022.1/models_bin/3/resnet50-binary-0001/FP32-INT1/resnet50-binary-0001.xml && \
   curl -O https://storage.openvinotoolkit.org/repositories/open_model_zoo/2022.1/models_bin/3/resnet50-binary-0001/FP32-INT1/resnet50-binary-0001.bin && \
   curl -O https://raw.githubusercontent.com/openvinotoolkit/model_server/main/demos/common/static/images/zebra.jpeg && \
   python3 classification_demo.py -m resnet50-binary-0001.xml -i zebra.jpeg --labels ../../../data/dataset_classes/imagenet_2012.txt --no_show -nstreams 1 -r"

```
