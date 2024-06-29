import os

label_dir = "/home/petmar/Documents/codes/yolo_demo/datasets/weeds/train/labels"

for label_name in os.listdir(label_dir):
    label_path = os.path.join(label_dir, label_name)
    with open(label_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                print(f"Invalid format in {label_path}: {line}")
