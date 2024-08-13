# Dockerfile generation for OpenVINO releases, for Ubuntu 20.04, Ubuntu 22.04, RHEL 8

## How to run

The tool does not require any non-standard Python packages, it only needs Python 3.10+ present

`configs/releases` directory contains configurations for all the supported releases. In general, if you want to build
`ubuntu20_dev:2024.3.0` image you should run this command:

```bash
python3 image.py 2024.3.0/ubuntu20 --preset dev --build
```
This will generate `Dockerfile` and build it, tagging it `localhost/ubuntu20_dev:2024.3.0`

## Current support state

Os support:
* Ubuntu 20: ✅
* Ubuntu 22: ✅
* Ubuntu 24: ❌
* RHEL8: ❌ (TODO)

OpenVINO releases support:
* before 2024.1.0 ❌
* 2024.1.0 ❌(TODO)
* 2024.2.0 ✅
* 2024.3.0 ✅

Device support:
* x86-64 CPU ✅
* aarch64 CPU ❌
* armhf CPU ❌
* Intel GPU ✅
* Intel NPU ✅

Note that even though `Intel NPU` is said to be supported it doesn't mean that every configuration supports it, for example `Ubuntu 20` doesn't support running on `Intel NPU`, only `Ubuntu 22` (and above when applicable) support it. Similar situation exists for Arm CPUs with Intel hardware.

## How to work with it

### When new OpenVINO release

1) Create a new release directory in `config/releases` called after the release version;
2) For each package build for specific os supported by this project, create a json file and use previous versions ad a template.

### When new OS needs to be supported

1) Create corresponding configs in the affected release directories
2) Create a base config for the new os

Try to use the previous os version configs as a template if applicable.

Note: some package versions are hard-coded or refer to a specific build, make sure those are also up-to-date for the new OS.

## How it works

### Config file structure

Configuration in this project is done with a chain of configs. Product configs are stored in `configs/releases`
directory, they inherit from base configs stored in `configs/base` which can also inherit from other base configs.
Config inheritance is defined with `_based_on` property, the config pointed at by `_based_on` will load first and then
the original config will merge with the base config.

Note: recursion is forbidden, that is, the dependency graph must have no cycles.

TODO: check for recursion, right now it will be infinitely loading if recursion appears.

#### Merging rules

1) If either object is null (or if either is missing / is undefined) then the other is returned
2) If objects have different types then an error is returned
3) If objects are dictionaries then they are merged with this algorithm
4) otherwise the new object is returned instead of the old one (including lists)

TODO: ^^^ describe merging better ^^^

Note: lists are not merged, they replace each other

This table shows a simplified example of how the files could be related to each other and how the merged
configuration would look like.

<style>
    table {
        border-width: 5px;
        border-style: solid
    }

    td {
        border-width: 3px;
        border-style: solid
    }
</style>
<table>
    <tbody>
        <tr>
            <td>common.json</td>
            <td>ubuntu.json</td>
            <td>ubuntu22.json</td>
            <td>releases/…/ubuntu22.json</td>
            <td>result (what will be read)</td>
        </tr>
        <tr>
            <td>{</td>
            <td>{</td>
            <td>{</td>
            <td>{</td>
            <td>{</td>
        </tr>
        <tr>
            <td></td>
            <td>"_based_on": "common"</td>
            <td>"_based_on": "ubuntu"</td>
            <td>"_based_on": "ubuntu22"</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>"_template": "Dockerfile.j2"</td>
            <td>"_template": "Dockerfile.j2"</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>"package": {</td>
            <td>"package": {</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>"url": "https://example.com"</td>
            <td>"url": "https://example.com"</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>"version": "2024.3.0"</td>
            <td>"version": "2024.3.0"</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>}</td>
            <td>}</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>"presets": {</td>
            <td>"presets": {</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>"runtime": ["preset_runtime", "device_gpu"]</td>
            <td>"runtime": ["preset_runtime", "device_gpu"]</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>…</td>
            <td>…</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>}</td>
            <td>}</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>"base_image": "ubuntu:22.04"</td>
            <td></td>
            <td>"base_image": "ubuntu:22.04"</td>
        </tr>
        <tr>
            <td>"components": {</td>
            <td>"components": {</td>
            <td>"components": {</td>
            <td></td>
            <td>"components": {</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>"intel-level-zero-gpu": {</td>
            <td></td>
            <td>"intel-level-zero-gpu": {</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>"requires": ["level-zero"]</td>
            <td></td>
            <td>"requires": ["level-zero"]</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>"apt": ["https://..."]</td>
            <td></td>
            <td>"apt": ["https://..."]</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>}</td>
            <td></td>
            <td>}</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>"level-zero": {</td>
            <td></td>
            <td>"level-zero": {</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>"apt": ["https://..."]</td>
            <td></td>
            <td>"apt": ["https://..."]</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>}</td>
            <td></td>
            <td>}</td>
        </tr>
        <tr>
            <td></td>
            <td>"base": {</td>
            <td></td>
            <td></td>
            <td>"base": {</td>
        </tr>
        <tr>
            <td></td>
            <td>"apt": ["curl", …]</td>
            <td></td>
            <td></td>
            <td>"apt": ["curl", …]</td>
        </tr>
        <tr>
            <td></td>
            <td>}</td>
            <td></td>
            <td></td>
            <td>}</td>
        </tr>
        <tr>
            <td>"preset_runtime": {</td>
            <td></td>
            <td></td>
            <td></td>
            <td>"preset_runtime": {</td>
        </tr>
        <tr>
            <td>"requires": ["base"]</td>
            <td></td>
            <td></td>
            <td></td>
            <td>"requires": ["base"]</td>
        </tr>
        <tr>
            <td>}</td>
            <td></td>
            <td></td>
            <td></td>
            <td>}</td>
        </tr>
        <tr>
            <td>"device_gpu": {</td>
            <td></td>
            <td></td>
            <td></td>
            <td>"device_gpu": {</td>
        </tr>
        <tr>
            <td>"requires": ["intel-level-zero-gpu", ...]</td>
            <td></td>
            <td></td>
            <td></td>
            <td>"requires": ["intel-level-zero-gpu", ...]</td>
        </tr>
        <tr>
            <td>}</td>
            <td></td>
            <td></td>
            <td></td>
            <td>}</td>
        </tr>
        <tr>
            <td>}</td>
            <td>}</td>
            <td>}</td>
            <td>}</td>
            <td>}</td>
        </tr>
        <tr>
            <td>}</td>
            <td>}</td>
            <td>}</td>
            <td>}</td>
            <td>}</td>
        </tr>
    </tbody>
</table>

