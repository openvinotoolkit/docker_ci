# OpenVINO™ Deep Learning Workbench

## Table of Contents

- [Introduction](#introduction)
- [System Requirements](#requirements)
- [Install DL Workbench](#install)
  - [Using Python wrapper](#wrapper)
  - [Using plain Docker command](#docker)
  - [DL Workbench Docker Image](#docker_image)
- [Useful Links](#links)

## <a id="introduction">Introduction</a>

Deep Learning Workbench is an official OpenVINO™ graphical user interface designed to make the production of pre-trained deep learning models significantly easier. 

The DL Workbench is an official UI environment of the OpenVINO™ toolkit that enables you to:

- Learn what neural networks are, how they work, and how to analyze their architectures and performance.
- Get familiar with the OpenVINO™ ecosystem and its main components without installing it on your system.
- Measure and interpret model performance.
- Analyze the quality of your model and visualize output.
- Optimize your model and prepare it for deployment on the target system.

In the DL Workbench, you can use the following OpenVINO™ toolkit components:

Component  |                 Description
|:------------------:|:------------------|
| [Open Model Zoo](https://docs.openvinotoolkit.org/latest/omz_tools_downloader.html)| Get access to the collection of high-quality pre-trained deep learning [public](https://docs.openvinotoolkit.org/latest/omz_models_group_public.html) and [Intel-trained](https://docs.openvinotoolkit.org/latest/omz_models_group_intel.html) models trained to resolve a variety of different tasks.  |
| [Model Optimizer](https://docs.openvinotoolkit.org/latest/openvino_docs_MO_DG_Deep_Learning_Model_Optimizer_DevGuide.html) |Optimize and transform models trained in supported frameworks to the IR format. <br>Supported frameworks include TensorFlow\*, Caffe\*, Kaldi\*, MXNet\*, and ONNX\* format.  
| [Benchmark Tool](https://docs.openvinotoolkit.org/latest/openvino_inference_engine_tools_benchmark_tool_README.html)| Estimate deep learning model inference performance on supported devices.
| [Accuracy Checker](https://docs.openvinotoolkit.org/latest/omz_tools_accuracy_checker.html) |Evaluate the accuracy of a model by collecting one or several metric values. 
| [Post-Training Optimization Tool](https://docs.openvinotoolkit.org/latest/pot_README.html)|Optimize pre-trained models with lowering the precision of a model from floating-point precision(FP32 or FP16) to integer precision (INT8), without the need to retrain or fine-tune models.                              |

## <a id="requirements">System Requirements</a>

The complete list of recommended requirements is available in the [documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Prerequisites.html).

To successfully run the DL Workbench with Python Starter, install Python 3.6 or higher.

Prerequisite | Linux* | Windows* | macOS*
:----- | :----- |:----- |:-----
Operating system|Ubuntu\* 18.04|Windows\* 10 | macOS\* 10.15 Catalina
Available RAM space| 8 GB\** | 8 GB\** | 8 GB\**
Available storage space| 10 GB + space for imported artifacts| 10 GB + space for imported artifacts| 10 GB + space for imported artifacts
Docker\*| Docker CE 18.06.1 | Docker Desktop 2.3.0.3|Docker CE 18.06.1

Windows\*, Linux\* and MacOS\* support CPU targets. GPU, Intel® Neural Compute Stick 2 and Intel® Vision Accelerator Design with Intel® Movidius™ VPUs are supported only for Linux\*.

## <a id="install">Install DL Workbench</a>

### <a id="wrapper">Install the DL Workbench Starter</a>

> LEGAL NOTICE: Your use of this software and any required dependent software (the “Software Package”) is subject to the terms and conditions of the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).

This section describes how to start the DL Workbench using the Python wrapper, which
works on Linux OS\*, macOS\* and Windows\*.
       
For additional details, such as prerequisites, security, and troubleshooting, see 
[OpenVINO DL Workbench documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Introduction.html).

#### Step 1. Set Up Python Virtual Environment

To avoid dependency conflicts, use a virtual environment. Skip this step only if you do want to install all dependencies globally.

Create virtual environment by executing the following commands in your terminal:

* On Linux and MacOS:
```
python3 -m pip install --user virtualenv
python3 -m venv venv
```
* On Windows:
```
py -m pip install --user virtualenv
py -m venv venv
```
#### Step 2. Activate Virtual Environment

* On Linux and MacOS:
```
source venv/bin/activate
```
* On Windows:
```
venv\Scripts\activate
```

#### Step 3. Update PIP to the Latest Version
Run the command below:

```
python -m pip install --upgrade pip
```
#### Step 4. Install the Python Wrapper
```
pip install -U openvino-workbench
```
#### Step 5. Verify the Installation

To verify that the package is properly installed, run the command below:
```
openvino-workbench --help
```
You will see the help message for the starting package if installation finished successfully.

#### Use the DL Workbench Starter

To start the latest available version of the DL Workbench, execute the following command:

```
openvino-workbench --image openvino/workbench:2021.3
```

You can see the list of available arguments with the following command:
```
openvino-workbench --help
```

Refer to the [documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Introduction.html) for additional information.

### <a id="docker"> Use web-form to build a starting command </a>

This section describes how to start the DL Workbench using the plain Docker\* command, which
works on Linux OS\*, macOS\* and Windows\*.
       
For additional details, such as prerequisites, security, and troubleshooting, see 
[OpenVINO DL Workbench documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Introduction.html).

#### Step 1. Navigate to the web-form website

* Web-form is available here: https://openvinotoolkit.github.io/workbench_aux/

#### Step 2. Select the necessary capabilities

* Go through the web-form interface and select the most suitable capabilities for you.

#### Step 3. Start DL Workbench

* Copy the resulting command and execute it in your terminal.

# <a id="docker_image">DL Workbench Docker Image</a>
  
  Pre-built DL Workbench Docker image is available on [Docker Hub*](https://hub.docker.com/repository/docker/openvino/workbench).

# <a id="links">Additional Resources</a>
* [Release Notes](https://software.intel.com/content/www/us/en/develop/articles/openvino-relnotes.html)
* [Documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Introduction.html)
* [Feedback](https://community.intel.com/t5/Intel-Distribution-of-OpenVINO/bd-p/distribution-openvino-toolkit)
* [Troubleshooting](https://community.intel.com/t5/Intel-Distribution-of-OpenVINO/bd-p/distribution-openvino-toolkit)

---
\* Other names and brands may be claimed as the property of others.
