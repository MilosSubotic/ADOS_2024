#!/usr/bin/env python

from roboflow import Roboflow

rf = Roboflow(api_key="<redacted>")
project = rf.workspace("<redacted>").project("<redacted>")
version = project.version(2)
dataset = version.download("yolov8")
