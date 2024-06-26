import cv2
import numpy as np
import glob
import os

image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/train/images/'  # Path to the directory with images

image_paths = glob.glob(os.path.join(image_dir, '*.*'))

for image_path in image_paths:

    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Failed to load image {image_path}")
        continue


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_blur = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, img.shape[0]/32, param1=210, param2=42, minRadius=10, maxRadius=300)

    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:

            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)


    cv2.imshow('Detected Circles', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
