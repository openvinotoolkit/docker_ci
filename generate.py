import subprocess
import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, ChainableUndefined

from lib import config, package_filename

TEMPLATE_ROOT = os.path.realpath(f"{__file__}/../templates")
jinjaenv = Environment(loader=FileSystemLoader(TEMPLATE_ROOT), undefined=ChainableUndefined)

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="Use pre-existing config to generate Dockerfile.")
parser.add_argument("--package_url", "--package-url", help="Generate config for given package url.")
parser.add_argument("--wheels_url", "--wheels-url", help="Also specify wheels url when generating the config.")
parser.add_argument("--os", help="Overwrite OS if package-url is given")
parser.add_argument("-p", "--preset", default="runtime", help="preset to build, e.g. 'dev' or 'runtime'")
parser.add_argument("--include-components",
    help="list of components to forcefully enable (separated by comma)")
parser.add_argument("--exclude-components", help="list of components to forcefully disable "
    "(separated by comma), Note: this option breaks component requirements")
parser.add_argument("-o", "--out", "--output", default="Dockerfile",
    help="output file name to write Dockerfile to, defaults to 'Dockerfile'")
parser.add_argument("-j", action="store_true", help="Also output a json with information about the image.")
parser.add_argument("--tests", action="store_true", help="Also generate test.sh that will run tests for the image")


args = parser.parse_args()

if args.config and args.package_url:
    raise Exception("Mutually exclusive options: package_url and config")

if not args.config and not args.package_url:
    raise Exception("Either package_url or config must be specified")


if args.config:
    context = config.default_env.load(args.config)
else:
    package_info = package_filename.parse(args.package_url.rsplit("/", 1)[-1])
    config_data = {
        "_based_on": args.os or package_info["os"],
        "_template": "Dockerfile_default.j2",
        "package": {
            "url": args.package_url,
            "version": package_info["version"],
            "distribution": package_info["dist"],
            "wheels": {
                "url": args.wheels_url,
            }
        }
    }
    context = config.default_env.from_dict(config_data)

include_components = args.include_components.split(",") if args.include_components else ()
exclude_components = args.exclude_components.split(",") if args.exclude_components else ()

context = config.process(
    context,
    args.preset,
    include_components=include_components,
    exclude_components=exclude_components
)

template = context["_template"]
dockerfile = jinjaenv.get_template(template).render(context)

with open(args.out, "w") as outfile:
    outfile.write(dockerfile)

image_name = f"{context['os_id']}_{args.preset}:{context['package']['version']}"

if args.j:
    with open("image_data.json", "w") as file:
        json.dump({
            "image_name": image_name,
            "base_image": context["base_image"],
            "product_version": context["package"]["version"],
            "wheels_version": None,
            "distribution": args.preset,
            "os": context["os_id"]
        }, file)

if args.tests:
    testfile = open("test.sh", "w")
    testfile.write("set -e\n")
    testfile.write(f"IMAGE_NAME={image_name}\n")
    testfile.write("TESTS_VOLUME=./refactor/tests/in_container:/tests\n")
    testfile.write('crun() { docker run --rm -it -v $TESTS_VOLUME $IMAGE_NAME bash -c "$1"; }\n')
    testfile.write('run_test() { echo TEST $1 $2; crun "/tests/$1 $2 2>&1 >/dev/null && echo SUCCESS || echo ERROR"; }\n')
    testfile.write("docker build -t $IMAGE_NAME .\n")
    for test in context["tests"]:
        arg = None
        try:
            test, arg = test.split("@", 1)
        except ValueError:
            pass
        testfile.write(f"run_test {test} {arg}\n")
