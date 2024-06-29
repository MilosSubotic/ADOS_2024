from ultralytics import YOLO
import os

model = YOLO("runs/detect/train5/weights/best.pt")

input_path = "detect/input"
output_path = "detect/output"

images = os.listdir(input_path)

for image_name in images:
    print(f"{image_name}:", end="")
    result = model(input_path + "/" + image_name)
    output_path_and_name = output_path + "/" + image_name
    result[0].save(filename = output_path_and_name)
