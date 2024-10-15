from sys import stdout, executable as python

import argparse
import subprocess
import json
import os

'''
This file is to provide limited support for older interface to run with old pipelines
'''

PROXY_ENV=["http_proxy", "https_proxy", "no_proxy"]
PROXY_ENV=map(lambda x: (x, os.environ.get(x)), PROXY_ENV)
PROXY_ENV=filter(lambda x: x[1], PROXY_ENV)
PROXY_ENV=list(PROXY_ENV)


parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("--package_url", "--package-url")
parser.add_argument("--wheels_url", "--wheels-url")
parser.add_argument("-os", "--os")
parser.add_argument("--nightly", action="store_true")
parser.add_argument("--preset", "-dist", "--dist", help="Preset to use")
parser.add_argument("-r", "--remote-repo", 
    help="Remote repo with registry, i.e. 'openvino-registry.iotg.sclab.intel.com/openvino'")
parser.add_argument("--source", help="either unset or 'local'")
parser.add_argument("-j", "--image_json_path", help="JSON file to output Image info to")

args = parser.parse_args()

assert args.command in ("all", "build")

if args.command == "all":
    assert args.remote_repo

if args.source:
    assert args.source == "local"

if args.image_json_path:
    assert args.image_json_path == "image_data.json"


def log_run(command):
    print(f"Running {command}")
    stdout.flush()
    subprocess.run(command).check_returncode()
    stdout.flush()


# Generate Dockerfile
command = [
    python, "generate.py",
    "--package-url", args.package_url,
    "--preset", args.preset,
    "-j"
]
if args.wheels_url:
    command.extend(["--wheels-url", args.wheels_url])
log_run(command)

image_info = json.load(open("image_data.json"))
image_name = image_info["image_name"]

# Build Dockerfile
if args.command == "all":
    log_run(["docker", "pull", image_info["base_image"]])

build_args_proxy = [f"--build-arg={k}={v}" for k, v in PROXY_ENV]

log_run(["docker", "build", ".", "-t", image_name, *build_args_proxy])

if args.command == "all":
    remote_name = f"{args.remote_repo}/{image_name}"
    log_run(["docker", "tag", image_name, remote_name])
    log_run(["docker", "push", remote_name])