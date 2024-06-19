#!/usr/bin/env python3

from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt") 

# Train the model
results = model.train(
	data = "data.yaml",
	imgsz = 768,
	#epochs = 100,
	epochs = 10,
	batch = -1,
	plots = True
)

