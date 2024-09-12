import subprocess
import tempfile
import uuid
import sys
import os

import pytest

from lib.config import default_env


def test_runs_without_virtualenv():
    # the idea is that the script runs without any extra modules
    # the best way that came to my mind

    environ = os.environ.copy()
    if "VIRTUAL_ENV" in environ:
        del environ["VIRTUAL_ENV"]
    subprocess.check_call(
        args=[os.path.realpath(sys.executable), "generate.py", "--help"],
        env=environ
    )


@pytest.fixture(scope="session")
def temp_dir():
    dir = tempfile.TemporaryDirectory(prefix="pytest_")
    yield dir.name
    dir.cleanup()
    del dir


@pytest.fixture
def temp_file(temp_dir):
    files = []
    def new_file(name):
        new_name = temp_dir + "/" + name + "_" + uuid.uuid4().hex[:10]
        files.append(new_name)
        return new_name
    yield new_file
    for file in files:
        os.remove(file)


def parametrize_config_preset():
    for conf in default_env.discover():
        conf_data = default_env.load(conf)
        if not "presets" in conf_data:
            continue
        for preset in conf_data["presets"]:
            yield (conf, preset)
    return []


@pytest.mark.parametrize('config,preset', parametrize_config_preset())
def test_dockerfile_generate(config, preset, temp_file):
    dockerfile = temp_file("Dockerfile")
    subprocess.check_call([sys.executable, "image.py", config, "-p", preset, "-o", dockerfile])
