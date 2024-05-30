#!/usr/bin/env python3

from ultralytics import YOLO

# Load a model
model = YOLO("runs/detect/train/weights/best.pt") 

results = model([
	"../../../../Agriculture_Machinery_Data_Heavy/Cherry_Picker_Arm/Media/lego/1715890560879.jpg",
	"../../../../Agriculture_Machinery_Data_Heavy/Cherry_Picker_Arm/Media/lego/1715890560960.jpg"
])

for result in results:
	result.show()