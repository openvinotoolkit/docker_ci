# Tutorials for [Intel® Distribution of OpenVINO™ toolkit](https://github.com/openvinotoolkit/openvino) Docker images

This folder contains some tutorials to demonstrate usage of OpenVINO™ Docker containers.

## List of tutorials

* **OV_docker_usage.ipynb** - Jupyter* Notebook tutorial will go step-by-step to demonstrate how to use OpenVINO™ Docker containers
* **OV_docker_VScode.md** - Markdown* tutorial will go step-by-step to demonstrate debugging using OpenVINO™ custom development Docker container and Visual Studio Code* integration.

## How to follow the Jupyter tutorial

You need to have [docker engine](https://docs.docker.com/) installed on the host with permissions to run docker commands.

You must also install Jupyter notebook via pip `pip install notebook`.

Clone the git repository and start the Jupyter notebook via a command:

```
git clone https://github.com/openvinotoolkit/docker_ci
jupyter-notebook --notebook-dir docker_ci/docs/tutorials/
```

---
\* Other names and brands may be claimed as the property of others.
