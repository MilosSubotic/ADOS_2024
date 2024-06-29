import cv2
import numpy as np
import yaml
import os

current_image_index = 0
image_files = []

def load_hsv_ranges(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

def load_images(folder_path):
    global image_files
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.JPG'))]

def process_current_image():
    global current_image_index, image_files, hsv_image

    image_path = os.path.join(folder_path, image_files[current_image_index])
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not open or find the image: {image_files[current_image_index]}")
        return

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_data = load_hsv_ranges(yaml_file)

    labels = []
    height, width, _ = image.shape

    for cls in hsv_data['classes']:
        class_id = cls['class_id']
        size = cls['min_size']
        lower_bound = np.array([cls['H']['start'], cls['S']['start'], cls['V']['start']])
        upper_bound = np.array([cls['H']['stop'], cls['S']['stop'], cls['V']['stop']])

        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > int(size):
                x, y, w, h = cv2.boundingRect(contour)
                center_x = (x + w / 2) / width
                center_y = (y + h / 2) / height
                bbox_w = w / width
                bbox_h = h / height
                labels.append(f"{class_id} {center_x} {center_y} {bbox_w} {bbox_h}")

        annotation_path = os.path.join(label_path, os.path.splitext(image_files[current_image_index])[0] + '.txt')
        with open(annotation_path, 'w') as f:
            f.write("\n".join(labels))


folder_path = 'datasets/train/images'
label_path = 'datasets/train/labels'
yaml_file = 'HSV_Thresholds.cfg.yaml'

load_images(folder_path)

for i in range(len(image_files)):
    process_current_image()
    current_image_index += 1
