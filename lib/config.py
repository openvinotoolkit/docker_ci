import json
import os

from lib import package_filename


class _ConfDir:
    def __init__(self, root_dir):
        self.root_dir = root_dir
    
    def get(self, name):
        with open(f"{self.root_dir}/{name}.json") as conf_file:
            conf = json.load(conf_file)
            assert isinstance(conf, dict), "Config must be dict"
            return conf


class Env:
    def __init__(self, product_dir, config_dir):
        self.product_dir = product_dir
        if isinstance(config_dir, _ConfDir):
            self.config_dir = config_dir
        else:
            self.config_dir = _ConfDir(config_dir)
    
    @staticmethod
    def merge_values(old, new):
        if old is None:
            return new
        if new is None:
            return old
        if old.__class__ != new.__class__:
            raise Exception(f"Config merge error: {old.__class__} and {new.__class__} are incompatible")
        if isinstance(old, dict):
            keys = list(old.keys())
            keys.extend([
                key
                for key in new.keys()
                if key not in old.keys()
            ])
            return {
                key: Env.merge_values(old.get(key), new.get(key))
                for key in keys
            }
        if isinstance(old, list):
            print(f"Warning: lists are replaced, not merged: {old}")
        return new


    def _load(self, initial_conf):
        base = initial_conf
        cascade = []
        while base:
            if "_based_on" in base:
                new_base_name = base["_based_on"]
                del base["_based_on"]
                cascade.append(base)
                base = self.config_dir.get(new_base_name)
            else:
                cascade.append(base)
                base = None
        result = {}
        for item in cascade[::-1]:
            result = self.merge_values(result, item)
        return result

    def load(self, product):
        # TODO: if valid path is given instead of a product, use it
        with open(f"{self.product_dir}/{product}.json") as prodconf:
            return self._load(json.load(prodconf))
        
    def from_dict(self, data):
        return self._load(data)

    def discover(self):
        for product_name in os.scandir(self.product_dir):
            if not product_name.is_dir():
                continue
            for product_conf in os.scandir(product_name.path):
                if not product_conf.name.endswith(".json"):
                    continue
                yield f"{product_name.name}/{product_conf.name.rsplit('.', 1)[0]}"

CONFIGS_ROOT = os.path.realpath(f"{__file__}/../../configs")
default_env = Env(f"{CONFIGS_ROOT}/releases", f"{CONFIGS_ROOT}/base")


def process(config, preset, include_components=(), exclude_components=()):
    # enable --include-components
    for component in include_components:
        config["components"][component]["enable"] = True

    # enable components of the selected preset
    for component in config["presets"][preset]:
        config["components"][component]["enable"] = True

    # enable all subcomponents
    def enable_recursively(components, cname):
        components[cname]["enable"] = True
        subcomponents = components[cname].get("requires")
        if not subcomponents:
            return
        for subcomponent in subcomponents:
            enable_recursively(components, subcomponent)

    for cname, component in config["components"].items():
        enabled = component.get("enable")
        if not enabled:
            continue
        enable_recursively(config["components"], cname)

    # disable --exclude-components
    for component in exclude_components:
        config["components"][component]["enable"] = False


    # collect apt packages
    apt_packages = []
    apt_downloads = []
    for cname, component in config["components"].items():
        if not component.get("enable"):
            continue
        apt = component.get("apt")
        if not apt:
            continue
        for package in apt:
            if package.startswith("https://"):
                filename = package.rsplit("/", 1)[-1]
                filepath = "/tmp/apt_dl/{}".format(filename)
                apt_downloads.append((package, filepath))
            else:
                apt_packages.append(package)

    config["apt"] = {
        "packages": apt_packages,
        "downloads": apt_downloads,
        "download_dir": "/tmp/apt_dl"
    }

    # collect rpm packages
    rpm_packages = []
    for cname, component in config["components"].items():
        if not component.get("enable"):
            continue
        rpm = component.get("rpm")
        if not rpm:
            continue
        rpm_packages.extend(rpm)
    
    config["rpm"] = {
        "packages": rpm_packages
    }

    assert bool(config["rpm"]["packages"]) ^ \
        bool(config["apt"]["packages"] or config["apt"]["downloads"]), \
        "Can't be both rpm and apt based system. Something's wrong"

    # collect tests
    tests = set()
    for cname, component in config["components"].items():
        if not component.get("enable"):
            continue
        comp_tests = component.get("tests")
        if comp_tests and isinstance(comp_tests, list):
            tests.update(comp_tests)

    config["tests"] = list(tests)

    return config
