#!/usr/bin/env python3

from ultralytics import YOLO
import glob
import cv2

# Load a model
model = YOLO("./runs/detect/train/weights/best.pt")

# Prepare images path
imgs = glob.glob('./dataset/images/test/*.jpg')

# Saves images and labels to /dataset/runs/train/predict
results = model.predict(source=imgs, save=True, save_txt=True, conf=0.5)