#!/bin/bash

ldd -u $(find -name $1) >/dev/null
