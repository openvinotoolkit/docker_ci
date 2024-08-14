#!/bin/bash

ldd $(find -name $1) | grep "not found" && exit 1 || exit 0
