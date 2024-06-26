import os
import glob
import cv2
import yaml
from os.path import join, basename, splitext

cfg_file = 'HSV_Thresholds.cfg.yaml'
images_dir = 'dataset/images/'
labels_dir = 'dataset/gen_labels/'
classes_file = 'dataset/classes.txt'

# Load HSV thresholds from YAML config
with open(cfg_file, 'r') as f:
    cfg = yaml.safe_load(f)

# Function to apply HSV thresholding and save labels in YOLO format
def apply_hsv_threshold(img_path, label_path, thresholds):
    # Load image
    img = cv2.imread(img_path)
    if img is None:
        print(f'Error: Failed to load image {img_path}')
        return
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Initialize list to store labels for YOLO format
    labels = []
    class_ids = set()  # Set to store unique class IDs
    
    # Get thresholds for each class
    for class_info in thresholds['classes']:
        class_id = class_info['class_id']
        class_name = class_info['class_name']
        H_range = class_info['H_quality']
        S_range = class_info['S_quality']
        V_range = class_info['V_quality']
        
        # Define HSV ranges
        lower_hsv = (H_range['start'], S_range['start'], V_range['start'])
        upper_hsv = (H_range['stop'], S_range['stop'], V_range['stop'])
        
        # Create mask using HSV thresholds
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Process each contour (object) found
        for contour in contours:
            # Get bounding box coordinates and dimensions
            x, y, w, h = cv2.boundingRect(contour)
            
            # Normalize bounding box coordinates to range [0, 1]
            img_height, img_width, _ = img.shape
            center_x = (x + w / 2) / img_width
            center_y = (y + h / 2) / img_height
            bbox_width = w / img_width
            bbox_height = h / img_height
            
            # Append label in YOLO format to list
            labels.append(f"{class_id} {center_x} {center_y} {bbox_width} {bbox_height}")
            class_ids.add(class_id)  # Add class_id to set of class IDs
    
    # Write labels to file in YOLO format
    with open(label_path, 'w') as f:
        f.write("\n".join(labels) + "\n")
    
    return class_ids

# Iterate over 'train', 'val', 'test', 'trash' directories
all_class_ids = set()
for subdir in ['train', 'val', 'test', 'trash']:
    images_subdir = join(images_dir, subdir)
    labels_subdir = join(labels_dir, subdir)
    os.makedirs(labels_subdir, exist_ok=True)
    
    # Iterate over each image in the current 'subdir'
    for img_path in glob.glob(join(images_subdir, '*.jpg')):
        img_filename = basename(img_path)
        img_name, img_ext = splitext(img_filename)
        label_path = join(labels_subdir, img_name + ".txt")
        
        # Apply HSV thresholding and save labels in YOLO format
        class_ids = apply_hsv_threshold(img_path, label_path, cfg)
        all_class_ids.update(class_ids)

# Write classes.txt file
with open(classes_file, 'w') as f:
    for class_id in sorted(all_class_ids):
        for class_info in cfg['classes']:
            if class_info['class_id'] == class_id:
                f.write(f"{class_info['class_name']}\n")

print("Labeling and classes file generation complete.")


# #!/usr/bin/env python3


# cfg = 'HSV_Thresholds.cfg.yaml'
# labeler = 'OpenCV/HSV/build/HSV_Labeler'
# images_dir = 'dataset/images/'
# labels_dir = 'dataset/gen_labels/'



# import os
# import glob
# import subprocess
# import shutil
# from os.path import *

# def run_cmd(cmd):
# 	r = subprocess.run(cmd.split())
# 	if r.returncode != 0:
# 		error('failed cmd:', cmd)


# for subdir in ['train', 'val', 'test', 'trash']:
# 	images_subdir = join(images_dir, subdir)
# 	labels_subdir = join(labels_dir, subdir)
# 	os.makedirs(labels_subdir, exist_ok = True)
# 	for img in glob.glob(join(images_subdir, '*.jpg')):
# 		b = basename(img)
# 		c, e = splitext(b)
# 		label = join(labels_subdir, c + ".txt")
# 		run_cmd(f'{labeler} {cfg} {img} {label}')


