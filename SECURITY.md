## Security guideline

Before commit to our repository please scan code on security vulnerabilities via [bandit tool](https://github.com/PyCQA/bandit).
Run [snyk scan](https://github.com/snyk/snyk) on code and on a docker image if you do changes in dockerfile.

Before target using a docker container, please update third-party packages to get the last security fixes. 
It needs because an docker image has 3d party snapshot on the time that it was built. 
When you will use a docker container based on the image, several new security vulnerabilities may be already fixed and need just update these 3d party packages.
```cmd
# for Ubuntu
apt update && apt upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# for RHEL
yum -y update-minimal --security --setopt=tsflags=nodocs && yum clean all
```
We recommend to use the latest version of PyPi packages installer to resolve dependency issues as well.
```cmd
python -m pip install --upgrade pip
```
As well we recommend to use the official Intel® Distribution of OpenVINO™ toolkit packages from trusted resources. 
See more on the [product page](https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/choose-download.html).

## Report a Vulnerability 

Please report security issues or vulnerabilities to the [Intel® Security Center](https://www.intel.com/security).
For more information on how Intel® works to resolve security issues, see
[Vulnerability Handling Guidelines](https://www.intel.com/content/www/us/en/security-center/vulnerability-handling-guidelines.html).
