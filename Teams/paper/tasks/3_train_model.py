#!/usr/bin/env python3

from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt") 

# Train the model
results = model.train(
	data = "./cfg/data.yaml",
	imgsz = 640,
	#epochs = 100,
	epochs = 10,
	batch = 8,
    workers = 4,
	plots = True
)