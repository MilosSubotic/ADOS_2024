#!/usr/bin/env python3

from ultralytics import YOLO
import glob

# Load a model
model = YOLO("./runs/detect/train2/weights/best.pt")

# Prepare images path
imgs = glob.glob('./dataset/images/test/*.jpg')

# Gets predicted images with labels and saves them
results = model.predict(source=imgs, save=True, save_txt=True, conf=0.5)