import cv2
import numpy as np
import os

base_dir = '/home/tonke9/ADOS24/ADOS_2024/kultura+korov/dataset/'
dirs = {
    'train_images': os.path.join(base_dir, 'train/images'),
    'train_labels': os.path.join(base_dir, 'train/labels'),
    'valid_images': os.path.join(base_dir, 'valid/images'),
    'valid_labels': os.path.join(base_dir, 'valid/labels')
}

for label_dir in dirs.values():
    if 'labels' in label_dir:
        os.makedirs(label_dir, exist_ok=True)

hsv_thresholds = {
    'soja': {'hMin': 60, 'hMax': 80, 'sMin': 80, 'sMax': 255, 'vMin': 0, 'vMax': 255},
    'korov': {'hMin': 35, 'hMax': 50, 'sMin': 80, 'sMax': 255, 'vMin': 0, 'vMax': 255}
}

def process_image(image_path, label_dir):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    all_boxes = []
    for class_id, (class_name, thresholds) in enumerate(hsv_thresholds.items()):
        lower = np.array([thresholds['hMin'], thresholds['sMin'], thresholds['vMin']])
        upper = np.array([thresholds['hMax'], thresholds['sMax'], thresholds['vMax']])
        mask = cv2.inRange(hsv, lower, upper)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            all_boxes.append((x, y, x + w, y + h, class_id))

    save_labels(image_path, all_boxes, img.shape, label_dir)

def save_labels(image_path, boxes, img_shape, label_dir):
    base_name = os.path.basename(image_path)
    core_name, _ = os.path.splitext(base_name)
    label_path = os.path.join(label_dir, core_name + ".txt")
    
    height, width, _ = img_shape
    with open(label_path, 'w') as f:
        for (ix, iy, ex, ey, class_id) in boxes:
            x_center = (ix + ex) / 2 / width
            y_center = (iy + ey) / 2 / height
            bbox_width = (ex - ix) / width
            bbox_height = (ey - iy) / height
            f.write(f'{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n')

for phase in ['train', 'valid']:
    image_dir = dirs[f'{phase}_images']
    label_dir = dirs[f'{phase}_labels']
    image_files = os.listdir(image_dir)
    for image_name in image_files:
        if image_name.endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(image_dir, image_name)
            process_image(img_path, label_dir)

print("Processing complete.")
