import cv2
import numpy as np
import os
import glob

image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/train/images/' 

annotation_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/train/labels'

os.makedirs(annotation_dir, exist_ok=True)

image_paths = glob.glob(os.path.join(image_dir, '*.*'))

color_ranges = {
    'black': ([0, 0, 0], [180, 255, 45]),
    'white': ([0, 0, 240], [180, 111, 255]),
    'red': ([159, 50, 70], [180, 255, 255]),
    'green': ([36, 50, 70], [89, 255, 255]),
    'blue': ([90, 50, 70], [128, 255, 255]),
    'yellow': ([25, 50, 70], [35, 255, 255]),
    'orange': ([9, 100, 100], [29, 255, 255])
}

# Ovaj deo koda samo za hsv, za robo izbrisati
class_map = {
    'black': 0,
    'white': 1,
    'red': 2,
    'green': 3,
    'blue': 4,
    'yellow': 5,
    'orange': 6
}

def save_yolo_annotation(image_path, boxes, image_width, image_height):
    annotation_file = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
    with open(os.path.join(annotation_dir, annotation_file), 'w') as f:
        for box in boxes:
            class_idx = box[0]
            x_center = ((box[1] + box[3]) / 2.0) / image_width
            y_center = ((box[2] + box[4]) / 2.0) / image_height
            width = (box[3] - box[1]) / image_width
            height = (box[4] - box[2]) / image_height
            f.write(f"{class_idx} {x_center} {y_center} {width} {height}\n")

for image_path in image_paths:
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image {image_path}")
        continue

    image_height, image_width = image.shape[:2]

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(gray_image, 5)
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, gray_image.shape[0]/32, param1=210, param2=42, minRadius=10, maxRadius=300)

    circle_mask = np.zeros_like(gray_image)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(circle_mask, (x, y), r, 255, thickness=-1)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    boxes = []

    for color, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        color_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        mask_final = cv2.bitwise_and(color_mask, circle_mask)

        kernel = np.ones((5, 5), np.uint8)
        mask_final = cv2.morphologyEx(mask_final, cv2.MORPH_CLOSE, kernel)
        mask_final = cv2.morphologyEx(mask_final, cv2.MORPH_OPEN, kernel)

        num_labels, labels_im = cv2.connectedComponents(mask_final)

        for i in range(1, num_labels):
            points = np.argwhere(labels_im == i)
            x_min, y_min = points.min(axis=0)
            x_max, y_max = points.max(axis=0)
            boxes.append((class_map[color], x_min, y_min, x_max, y_max))

    save_yolo_annotation(image_path, boxes, image_width, image_height)

    # Display the result (optional)
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Mask', mask_final)
    # cv2.imshow('Labeled Image', labels_im)
    # cv2.waitKey(0)

cv2.destroyAllWindows()
