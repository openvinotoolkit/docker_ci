import re

PACKAGE_FILENAME_RE = re.compile(
    r"^([lmw])?_?openvino_(toolkit|genai|tokenizers)"
    r"_?(dev|data_dev|runtime|ie_runtime)?"
    r"_(centos\d+|debian\d+|raspbian|rhel\d+|ubuntu\d+|macos_\d+_\d+|osx|windows|)"
    r"_?(arm|p|dev)?"
    r"_(20\d\d\.\d\.\d+).?([\.\da-z]+)?"
    r"_?(fpga_only|pot)?"
    r"_?(x86_64|armhf|arm64)?"
    r"\.(tgz|tar\.gz|zip)$"
)

FIELDS = (
    "os_fam_hint",  # l, w, m or None
    "dist",  # toolkit, genai or tokenizers
    "_subdist",  # deprecated; dev, data_dev, runtime or ie_runtime
    "os",  # centos*, debian*, raspbian, rhel*, ubuntu*, macos_*_*, osx, windows or ""
    "_prefix",  # deprecated; arm, p or dev
    "version",  # main version: three numbers
    "version_extra",  # extra version, no specific format
    "_version_suffix",  # deprecated; fpga_only or pot
    "arch",  # x86_64, armhf, arm64 or None
    "ext",  # tgz, tar.gz or zip
)

def parse(filename) -> dict:
    match = PACKAGE_FILENAME_RE.match(filename)
    if not match:
        return None
    return dict(zip(FIELDS, match.groups()))
