from ultralytics import YOLO
import os
import time

model = YOLO("runs/detect/train/weights/best.pt")

input_path = "runs/detect/input"
output_path = "runs/detect/output"

images = os.listdir(input_path)

for image_name in images:
    result = model(input_path + "/" + image_name)
    output_path_and_name = output_path + "/" + image_name
    result[0].save(filename = output_path_and_name)
