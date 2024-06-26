# HSV labeling example for Coca Cola can
import cv2
import numpy as np
import os

lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

images_path = "images/"
labels_path = "labels/"

images = os.listdir(images_path)

for img in images:
    image = cv2.imread(images_path + img)
    if image is None:
        print(f"Can't load image {img}")
        exit()

    # Convert to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Find required colors
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Find coordinates for label
    x, y, w, h = cv2.boundingRect(mask)

    # Normalizing coordinates for YOLO
    img_height, img_width, _ = image.shape
    x_center = (x + w / 2) / img_width
    y_center = (y + h / 2) / img_height
    w_norm = w / img_width
    h_norm = h / img_height

    label = f"0 {x_center} {y_center} {w_norm} {h_norm}"

    print(f"Label for {img}: {label}")

    output_file = labels_path + img + ".txt"

    with open(output_file, 'w') as f:
        f.write(label + "\n")

