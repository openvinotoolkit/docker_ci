## Security guideline

Before commit to our repository please scan code on security vulnerabilities via [bandit tool](https://github.com/PyCQA/bandit).
Run [snyk scan](https://github.com/snyk/snyk) on code and on a docker image if you do changes in dockerfile.

Before target using a docker container, please update third-party packages to get the last security fixes. 
It needs because an docker image has 3d party snapshot on the time that it was built. 
When you will use a docker container based on the image, several new security vulnerabilities may be already fixed and need just update these 3d party packages.
```cmd
apt update && apt upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*
```

As well we recommend to use the official Intel® Distribution of OpenVINO™ toolkit packages from trusted resources. 
See more on the [product page](https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/choose-download.html).

## Reporting a Vulnerability 

Please report (suspected) security vulnerabilities to
**[openvino_docker@intel.com](mailto:openvino_docker@intel.com)**. 

You will receive a response from
us within 48 hours. If the issue is confirmed, we will release a patch as soon
as possible depending on complexity but historically within a few days.