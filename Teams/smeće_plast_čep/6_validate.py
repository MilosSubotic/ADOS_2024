

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../Common/SW/"))
from common.utils import show

from ultralytics import YOLO

def val(model_pt):
    show(model_pt)
    model = YOLO(model_pt)
    metrics = model.val()  # no arguments needed, dataset and settings remembered
    show(metrics.box.map)  # map50-95
    show(metrics.box.map50)  # map50
    show(metrics.box.map75)  # map75
    show(metrics.box.maps)  # a list contains map50-95 of each category
    print()


#val("yolov8n.pt")
val("runs/detect/train6/weights/best.pt")
