# Configuration Guide for the Intel® Vision Accelerator Design with Intel® Movidius™ VPUs on Linux*

To use HDDL device in a docker container, previously setup HDDL daemon on the host machine:
1. Download/extract HDDL driver on the host. You can use a full OpenVINO package or [HDDL driver package](#download-hddl-driver-package) (small archive)
2. Run on the host machine with HDDL device from <archive_extract_folder>/hddl: 
```bash
source setupvars.sh && ./install_IVAD_VPU_dependencies.sh (reboot is required) 
source setupvars.sh && ./bin/hddldaemon -d 
```
Now the dependencies are installed and you are ready to use the Intel® Vision Accelerator Design with Intel® Movidius™ with the Intel® Distribution of OpenVINO™ toolkit.
You can inference on HDDL device in docker image without root privilege as well.

# Download HDDL driver package
You can use the official Intel® Distribution of OpenVINO™ toolkit packages from trusted resources.
See more on the [product page](https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/choose-download.html).

Or you can download a small archive of HDDL driver package from Amazon Web Services*.
Available releases for Ubuntu* 18.04:

*  [2020.2](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2020.2/hddl_ubuntu18_1076.tgz)
*  [2020.3](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2020.3/hddl_ubuntu18_1167.tgz)
*  [2020.3.1](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2020.3.1/hddl_ubuntu18_1409.tgz)
*  [2020.3.2](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2020.3.2/hddl_ubuntu18_1651.tgz)
*  [2020.4](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2020.4/hddl_ubuntu18_1229.tgz)
*  [2021.1](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2021.1/hddl_ubuntu18_1380.tgz)
*  [2021.2](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2021.2/hddl_ubuntu18_1509.tgz)
*  [2021.3](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2021.3/hddl_ubuntu18_1636.tgz)
*  [2021.4](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2021.4/hddl_ubuntu18_1701.tgz)
*  [2021.4.1](https://storage.openvinotoolkit.org/drivers/vpu/hddl/2021.4.1/hddl_ubuntu18_1701.tgz)

# Troubleshooting:

Please follow the [configuration guide for HDDL device](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux_ivad_vpu.html).

---
\* Other names and brands may be claimed as the property of others.