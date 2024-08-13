import subprocess
import argparse

from jinja2 import Environment, FileSystemLoader, ChainableUndefined

from lib import config


jinjaenv = Environment(loader=FileSystemLoader("templates"), undefined=ChainableUndefined)
confenv = config.Env("configs/releases", "configs/base")

parser = argparse.ArgumentParser()
parser.add_argument("config", help="release config to generate for, e.g. '2024.3.0/ubuntu20'")
parser.add_argument("-p", "-d", "--preset", default="runtime", help="preset to build, e.g. 'dev' or 'runtime'")
parser.add_argument("--include-components",
    help="list of components to forcefully enable (separated by comma)")
parser.add_argument("--exclude-components", help="list of components to forcefully disable "
    "(separated by comma), Note: this option breaks component requirements")
parser.add_argument("-o", "--out", "--output", default="Dockerfile",
    help="output file name to write Dockerfile to, defaults to 'Dockerfile'")
parser.add_argument("-b", "--build", action="store_true", help="also build the image and tag it with '{os}_{preset}:{version}'")
parser.add_argument("--test", action="store_true", help="also test the built image (implies --build option)")

args = parser.parse_args()

context = confenv.load(args.config)

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

if args.build or args.test:
    os_id = context["os_id"]
    package_version = context["package"]["version"]
    image_tag = f"localhost/{os_id}_{args.preset}:{package_version}"
    subprocess.run(["docker", "build", "-t", image_tag, "-f", args.out])

if args.test:
    for test_file in context["tests"]:
        print(f"Running {test_file} ...")
        arg = ""
        if "@" in test_file:
            test_file, arg = test_file.split("@", 1)
        result = subprocess.run([
            "docker", "run", "--rm",
            "-v", "./tests:/tests",
            "--device", "/dev/dri",
            # "--device", "/dev/accel",
            image_tag,
            "bash", "-c", f"/tests/{test_file} {arg}"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("FAILED")
        else:
            print("PASSED")
