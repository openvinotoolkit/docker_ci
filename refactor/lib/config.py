import json
import os


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
            print("Warning: lists are replaced, not merged")
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

    def discover(self):
        for product_name in os.scandir(self.product_dir):
            if not product_name.is_dir():
                continue
            for product_conf in os.scandir(product_name.path):
                if not product_conf.name.endswith(".json"):
                    continue
                yield f"{product_name.name}/{product_conf.name.rsplit('.', 1)[0]}"


def process(config, preset):
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


    # collect apt packages
    apt_packages = []
    apt_downloads = []
    for cname, component in config["components"].items():
        enabled = component.get("enable")
        if not enabled:
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

    return config
