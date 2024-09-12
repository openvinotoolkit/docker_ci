import pytest
import json
import os

from urllib.request import Request, urlopen


def parametrize_configs(path):
    to_scan = [path]
    while to_scan:
        for item in os.scandir(to_scan.pop()):
            if item.is_dir():
                to_scan.append(item.path)
                continue
            if item.name.endswith(".json"):
                yield item.path


@pytest.mark.parametrize('path', parametrize_configs("configs"))
def test_valid_json(path):
    json.load(open(path))


@pytest.mark.parametrize('path', parametrize_configs("configs/releases"))
def test_package_url_exists(path):
    data = json.load(open(path))
    package = data.get("package")
    if not package:
        pytest.skip("no package defined")
    package_url = package.get("url")
    if not package_url:
        raise Exception("package defined, but no url")
    urlopen(Request(package_url, method="HEAD"))
