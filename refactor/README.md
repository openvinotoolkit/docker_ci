# Dockerfile generation for OpenVINO releases, for Ubuntu 20.04, Ubuntu 22.04, RHEL 8

## How to run

The tool does not require any non-standard Python packages, it only needs Python 3.10+ present

```bash
python3 image.py 2024.3.0/ubuntu20 --preset dev --build
```

This will generate `Dockerfile` and build it, tagging it `localhost/ubuntu20_dev:2024.3.0`