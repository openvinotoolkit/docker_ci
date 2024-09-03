#!/bin/bash

set -e
ldd $(find -name $1) 2>/dev/null
ldd $(find -name $1) 2>/dev/null | grep "not found" && exit 1 || exit 0
