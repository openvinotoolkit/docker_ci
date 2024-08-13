#!/bin/bash

set -e

omz_downloader --name yolo-v1-tiny-tf
benchmark_app -m public/yolo-v1-tiny-tf/yolo-v1-tiny.pb -shape [1,416,416,3] -t 1

ovc public/yolo-v1-tiny-tf/yolo-v1-tiny.pb
benchmark_app -m yolo-v1-tiny.xml -shape [1,416,416,3] -t 1
