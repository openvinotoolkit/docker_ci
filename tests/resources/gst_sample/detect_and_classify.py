# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import sys
from argparse import ArgumentParser

import gi
from gi.repository import Gst, GstVideo
from gstgva import VideoFrame, util

gi.require_version('GstVideo', '1.0')
gi.require_version('Gst', '1.0')

DETECT_THRESHOLD = 0.5

Gst.init(sys.argv)


def ssd_process_frame(frame: VideoFrame, threshold: float = DETECT_THRESHOLD) -> bool:
    width = frame.video_info().width
    height = frame.video_info().height

    for tensor in frame.tensors():
        dims = tensor.dims()
        data = tensor.data()
        object_size = dims[-1]
        for i in range(dims[-2]):
            image_id = data[i * object_size + 0]
            label_id = data[i * object_size + 1]
            confidence = data[i * object_size + 2]
            x_min = int(data[i * object_size + 3] * width + 0.5)
            y_min = int(data[i * object_size + 4] * height + 0.5)
            x_max = int(data[i * object_size + 5] * width + 0.5)
            y_max = int(data[i * object_size + 6] * height + 0.5)

            if image_id != 0:
                break
            if confidence < threshold:
                continue

            frame.add_region(x_min, y_min, x_max - x_min, y_max - y_min, str(label_id), confidence)

    return True


def age_gend_class_process_frame(frame: VideoFrame) -> bool:
    for roi in frame.regions():
        for tensor in roi.tensors():
            if tensor.name() == 'detection':
                continue
            layer_name = tensor.layer_name()
            data = tensor.data()
            if 'age_conv3' == layer_name:
                tensor.set_label(str(int(data[0] * 100)))
                continue
            if 'prob' == layer_name:
                tensor.set_label(" M " if data[1] > 0.5 else " F ")
                continue
            if 'prob_emotion' == layer_name:
                emotions = ["neutral", "happy", "sad", "surprise", "anger"]
                tensor.set_label(emotions[data.index(max(data))])
                continue

    return True


parser = ArgumentParser(add_help=False)
_args = parser.add_argument_group('Options')
_args.add_argument("-i", "--input", help="Required. Path to input video file",
                   required=True, type=str)
_args.add_argument("-d", "--detection_model", help="Required. Path to an .xml file with object detection model",
                   required=True, type=str)
_args.add_argument("-c", "--classification_model",
                   help="Required. Path to an .xml file with object classification model",
                   required=True, type=str)


def detect_postproc_callback(pad, info):
    with util.GST_PAD_PROBE_INFO_BUFFER(info) as buffer:
        caps = pad.get_current_caps()
        frame = VideoFrame(buffer, caps=caps)
        status = ssd_process_frame(frame)
    return Gst.PadProbeReturn.OK if status else Gst.PadProbeReturn.DROP


def classify_postproc_callback(pad, info):
    with util.GST_PAD_PROBE_INFO_BUFFER(info) as buffer:
        caps = pad.get_current_caps()
        frame = VideoFrame(buffer, caps=caps)
        status = age_gend_class_process_frame(frame)
    return Gst.PadProbeReturn.OK if status else Gst.PadProbeReturn.DROP


def main():
    args = parser.parse_args()

    # init GStreamer
    Gst.init(None)

    # build pipeline using parse_launch
    pipeline_str = f"""\
    filesrc location={args.input} ! decodebin ! videoconvert ! video/x-raw,format=BGRx ! \
    gvainference name=gvainference model={args.detection_model} ! queue ! \
    gvaclassify name=gvaclassify model={args.classification_model} ! queue ! gvafpscounter ! \
    fakesink async = false """

    pipeline = Gst.parse_launch(pipeline_str)

    # set callbacks
    gvainference = pipeline.get_by_name('gvainference')
    if gvainference:
        pad = gvainference.get_static_pad('src')
        pad.add_probe(Gst.PadProbeType.BUFFER, detect_postproc_callback)

    gvaclassify = pipeline.get_by_name('gvaclassify')
    if gvaclassify:
        pad = gvaclassify.get_static_pad('src')
        pad.add_probe(Gst.PadProbeType.BUFFER, classify_postproc_callback)

    # start pipeline
    pipeline.set_state(Gst.State.PLAYING)

    # wait until EOS or error
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

    # free pipeline
    pipeline.set_state(Gst.State.NULL)


if __name__ == '__main__':
    sys.exit(main() or 0)
