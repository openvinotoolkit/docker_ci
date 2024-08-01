import subprocess
import argparse

from jinja2 import Environment, FileSystemLoader

from lib import config


jinjaenv = Environment(loader=FileSystemLoader("templates"))
confenv = config.Env("configs/releases", "configs/base")

# load merged config
parser = argparse.ArgumentParser()
parser.add_argument("config", help="release config to generate for, e.g. '2024.3.0/ubuntu20'")
parser.add_argument("-p", "-d", "--preset", default="runtime", help="preset to build, e.g. 'dev' or 'runtime'")
parser.add_argument("-o", "--out", "--output", default="Dockerfile",
    help="output file name to write Dockerfile to, defaults to 'Dockerfile'")
parser.add_argument("-b", "--build", action="store_true", help="also build the image and tag it with '{os}_{preset}:{version}'")
args = parser.parse_args()

context = confenv.load(args.config)
context = config.process(context, args.preset)

template = context["_template"]
dockerfile = jinjaenv.get_template(template).render(context)

with open(args.out, "w") as outfile:
    outfile.write(dockerfile)

if args.build:
    os_id = context["os_id"]
    package_version = context["package"]["version"]
    image_tag = f"localhost/{os_id}_{args.preset}:{package_version}"
    subprocess.run(["docker", "build", "-t", image_tag, "-f", args.out])
