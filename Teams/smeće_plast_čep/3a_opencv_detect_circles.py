import cv2
import numpy as np
import glob
import os

# Define the directory with images
image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/train/images/'  # Path to the directory with images

# Find all images in the directory (jpg, png, etc.)
image_paths = glob.glob(os.path.join(image_dir, '*.*'))

# Process each image in the directory
for image_path in image_paths:
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Failed to load image {image_path}")
        continue

    # Convert to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image to reduce noise
    img_blur = cv2.medianBlur(gray, 5)
    # Apply hough transform on the image
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, img.shape[0]/32, param1=210, param2=42, minRadius=10, maxRadius=300)

    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw inner circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

    # Display the results (optional)
    cv2.imshow('Detected Circles', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
