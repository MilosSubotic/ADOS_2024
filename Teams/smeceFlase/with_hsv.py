#!/usr/bin/env python3

import os
import glob
import cv2
import numpy as np
import yaml

cfg = 'C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/HSV_Thresholds.cfg.yaml'
images_dir = 'C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/dataset/images'
labels_dir = 'C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/dataset/gen_labels'

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def process_image(image_path, classes):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image {image_path}")
        return []

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    labels = []

    for cls in classes:
        class_name = cls['class_name']
        class_id = cls['class_id']
        bb_color = cls['bb_color']
        H_range = (cls['H']['start'], cls['H']['stop'])
        S_range = (cls['S']['start'], cls['S']['stop'])
        V_range = (cls['V']['start'], cls['V']['stop'])

        if H_range[0] > H_range[1]:
            lower_bound1 = np.array([H_range[0], S_range[0], V_range[0]])
            upper_bound1 = np.array([179, S_range[1], V_range[1]])
            lower_bound2 = np.array([0, S_range[0], V_range[0]])
            upper_bound2 = np.array([H_range[1], S_range[1], V_range[1]])
            mask1 = cv2.inRange(hsv_image, lower_bound1, upper_bound1)
            mask2 = cv2.inRange(hsv_image, lower_bound2, upper_bound2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower_bound = np.array([H_range[0], S_range[0], V_range[0]])
            upper_bound = np.array([H_range[1], S_range[1], V_range[1]])
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            labels.append((class_id, x, y, x + w, y + h))
    
    return labels

def save_labels(label_path, labels):
    with open(label_path, 'w') as file:
        for label in labels:
            class_id, x_min, y_min, x_max, y_max = label
            file.write(f"{class_id} {x_min} {y_min} {x_max} {y_max}\n")

# Read configuration from YAML file
config = read_yaml(cfg)

# Process each image in the dataset
for subdir in ['train', 'val', 'test']:
    images_subdir = os.path.join(images_dir, subdir)
    labels_subdir = os.path.join(labels_dir, subdir)
    os.makedirs(labels_subdir, exist_ok=True)

    for img in glob.glob(os.path.join(images_subdir, '*.jpg')):
        base_name = os.path.basename(img)
        label_name = os.path.splitext(base_name)[0] + ".txt"
        label_path = os.path.join(labels_subdir, label_name)

        # Process image and generate labels
        labels = process_image(img, config['classes'])
        # Save labels to file
        save_labels(label_path, labels)
        print(f"Labeled {img} and saved to {label_path}")
