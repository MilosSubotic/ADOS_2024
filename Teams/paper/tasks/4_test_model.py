#!/usr/bin/env python3

from ultralytics import YOLO
import glob

# Load a model
model = YOLO("./runs/detect/train2/weights/best.pt")

# Get all images from path
imgs = glob.glob('./dataset/images/test/*.jpg')

# Get result images with labels and save them
results = model.predict(source=imgs, save=True, save_txt=True, conf=0.5)

'''
 Predict parameters:

 source=imgs   - Specifies the data source for inference
 save=True     - Enables saving of the annotated images to file
 save_txt=True - Saves detection results in a text file, 
                 following the format: [class] [x_center] [y_center] [width] [height] [confidence]
 conf=0.5      - Sets the minimum confidence threshold for detections

'''
 