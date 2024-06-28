#!/usr/bin/env python3

from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")

# Train the model
results = model.train(
	data = "./cfg/data.yaml",
	imgsz = 640,   # Target image size for training
	epochs = 10,   # Total number of training epochs
	batch = 8,     # During each training iteration, a batch size of images will be processed before updating model's weights
    workers = 4,   # Number of worker threads for data loading
	plots = True   # Generates and saves plots of training and validation metrics, as well as prediction examples
)