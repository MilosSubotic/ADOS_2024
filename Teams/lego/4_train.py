#!/usr/bin/env python3

from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt") 

# Train the model
results = model.train(
    data="data.yaml",
    imgsz=640,
    epochs=10,
    plots=True
)

