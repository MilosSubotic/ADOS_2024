import cv2
import numpy as np
import os
import glob

image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/images/train/' 

image_paths = glob.glob(os.path.join(image_dir, '*.*'))

lower_red = np.array([36, 50, 70])
upper_red = np.array([89, 255, 255])

for image_path in image_paths:
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image {image_path}")
        continue

    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image_blur = cv2.medianBlur(image_grayscale, 5)

   
    circles = cv2.HoughCircles(image_blur, cv2.HOUGH_GRADIENT, 1, image.shape[0]/32, param1=210, param2=42, minRadius=10, maxRadius=300)

    circle_mask = np.zeros_like(image_grayscale)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            
            cv2.circle(circle_mask, (x, y), r, 255, thickness=-1)

    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

   
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    mask_final = cv2.bitwise_and(mask, circle_mask)

    num_labels, labels_im = cv2.connectedComponents(mask_final)

    labels_im = cv2.normalize(labels_im, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    cv2.imshow('Original Image', image)
    cv2.imshow("Circle Mask", circle_mask)
    cv2.imshow('Mask', mask_final)
    cv2.imshow('Labeled Image', labels_im)
    cv2.waitKey(0)

cv2.destroyAllWindows()
