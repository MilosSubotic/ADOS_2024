import cv2
import numpy as np
import os
import glob

image_dir = '/home/aleksandar/Desktop/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/train/images'  

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

for image_path in image_paths:
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image {image_path}")
        continue

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    final_labels = np.zeros(hsv_image.shape[:2], dtype=np.int32)
    label_count = 1

    for color, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        num_labels, labels_im = cv2.connectedComponents(mask)

        for i in range(1, num_labels):
            final_labels[labels_im == i] = label_count
            label_count += 1

    final_labels_normalized = cv2.normalize(final_labels, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    cv2.imshow('Original Image', image)
    cv2.imshow('Final Mask', final_labels_normalized)
    cv2.waitKey(0)

cv2.destroyAllWindows()
