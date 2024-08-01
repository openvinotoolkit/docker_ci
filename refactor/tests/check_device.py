#!/usr/bin/env python3
import sys
from subprocess import check_output
from os import readlink, scandir, access, W_OK


def readfile(path):
    with open(path) as f:
        return f.read().strip()
    

def cmd_out(*cmd, err=None):
    try:
        return check_output(cmd).decode().strip()
    except Exception:
        err = err or f"subcommand failed: {cmd}"
        print(f"ERROR: {err}")
        exit(-1)


try:
    _, arg = sys.argv
    arg = arg.upper()
except ValueError:
    print("ERROR: incorrect test call")
    exit(-1)


if arg == "CPU":
    cpu_arch = cmd_out("uname", "-m")
    if cpu_arch in ("x86_64", "aarch64"):
        print("PASSED")
        exit(0)
    else:
        print("FAILED: unknown arch")
        exit(-3)
elif arg == "GPU":
    intel_devices = []
    for dev in scandir("/sys/class/drm/"):
        if not dev.name.startswith("renderD"):
            continue
        dev_driver = readlink(f"{dev.path}/device/driver").rsplit("/", 1)[-1]
        if dev_driver == "i915":
            intel_devices.append(dev.name)
    if not intel_devices:
        print(f"FAILED: no intel devices found")
        exit(-3)
    for dev in intel_devices:
        ok = access(f"/dev/dri/{dev}", W_OK)
        if not ok:
            print(f"FAILED: no access to /dev/dri/{dev}")
            exit(-3)
    print("PASSED")
    exit(0)
elif arg == "NPU":
    intel_devices = []
    for dev in scandir("/sys/class/accel/"):
        dev_driver = readlink(f"{dev.path}/device/driver").rsplit("/", 1)[-1]
        if dev_driver == "intel_vpu":
            intel_devices.append(dev.name)
    if not intel_devices:
        print(f"FAILED: no intel devices found")
        exit(-3)
    for dev in intel_devices:
        ok = access(f"/dev/accel/{dev}", W_OK)
        if not ok:
            print(f"FAILED: no access to /dev/accel/{dev}")
            exit(-3)
    print("PASSED")
    exit(0)
else:
    print("ERROR: incorrect test call: unknown device")
    exit(-2)