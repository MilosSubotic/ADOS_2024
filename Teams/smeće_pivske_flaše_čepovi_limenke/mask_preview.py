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
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg'))]

def handle_key_event(key):
    global current_image_index, image_files

    if key == ord('n') and current_image_index < len(image_files) - 1:
        current_image_index += 1
        process_current_image()

    if key == ord('b') and current_image_index > 0:
        current_image_index -= 1
        process_current_image()

def process_current_image():
    global current_image_index, image_files, hsv_image

    image_path = os.path.join(folder_path, image_files[current_image_index])
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not open or find the image: {image_files[current_image_index]}")
        return

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hsv_data = load_hsv_ranges(yaml_file)
    result = image.copy()

    # Initialize a blank mask to combine all class masks
    combined_mask = np.zeros_like(hsv_image[:, :, 0])

    for cls in hsv_data['classes']:
        class_name = cls['class_name']
        class_id = cls['class_id']
        size = cls['min_size']
        bb_color = tuple(cls['bb_color'])
        lower_bound = np.array([cls['H']['start'], cls['S']['start'], cls['V']['start']])
        upper_bound = np.array([cls['H']['stop'], cls['S']['stop'], cls['V']['stop']])

        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        combined_mask = cv2.bitwise_or(combined_mask, mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > int(size):
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(result, (x, y), (x+w, y+h), bb_color, 2)
                cv2.putText(result, f"{class_name} {class_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, bb_color, 2)

    cv2.imshow('Original Image with Bounding Boxes', result)
    cv2.imshow('Mask', combined_mask)

folder_path = 'datasets/train/images'
yaml_file = 'HSV_Thresholds.cfg.yaml'

load_images(folder_path)
process_current_image()

while True:
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break
    handle_key_event(key)

cv2.destroyAllWindows()
