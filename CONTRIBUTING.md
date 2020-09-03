## How to Contribute
We welcome community contributions to the DockerHub CI framework for Intel® Distribution of OpenVINO™ toolkit repository.

Please read this document first. Thanks!
 
If you have an idea how to improve the product, please share it with us doing the following steps:

- Check code style ([PEP8](https://www.python.org/dev/peps/pep-0008/)). Code style is strictly enforced by CI rules with [flake8 tool](http://flake8.pycqa.org/en/latest/)
- Make static type check. Static type analysis is strictly enforced by CI rules with [mypy tool](http://mypy-lang.org/)
- Make sure you can build the docker image, run all tests with your patch
- In case of a larger feature, provide relevant unit tests
- Follow our [SECURITY](./SECURITY.md) guide
- Submit a pull request at https://github.com/openvinotoolkit/docker_ci/pulls

We will review your contribution and, if any additional fixes or modifications are necessary, may give some feedback to guide you. 
Your pull request will be merged into GitHub* repositories if accepted.

**Notes**:

If you fix a know submited issue, please mentioned its number in MR or directly in the footer of commit message (i.e. "Fixes #123")


We try to follow [Conventional Commits](https://www.conventionalcommits.org/) specification, please do too.