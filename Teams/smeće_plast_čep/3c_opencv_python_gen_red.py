import cv2
import numpy as np
import os
import glob

# Define the directory with images
image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/images/test/'  # Path to the directory with images

# Find all images in the directory (jpg, png, etc.)
image_paths = glob.glob(os.path.join(image_dir, '*.*'))

# Define HSV range for the target color (example for red color)
lower_red = np.array([25, 50, 70])
upper_red = np.array([35, 255, 255])

# Process each image in the directory
for image_path in image_paths:
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image {image_path}")
        continue

    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the red color
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Apply morphological operations (dilation and erosion)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=1, param1=50, param2=10, minRadius=10, maxRadius=200)

    # Create an empty mask for circles
    circle_mask = np.zeros_like(mask)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Draw circles on the mask
            cv2.circle(circle_mask, (x, y), r, (255), thickness=-1)

    # Combine the mask with circles with the original mask
    mask = cv2.bitwise_and(mask, circle_mask)

    # Label objects
    num_labels, labels_im = cv2.connectedComponents(mask)

    # Normalize labels for display
    labels_im = cv2.normalize(labels_im, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Display the results
    cv2.imshow('Original Image', image)
    cv2.imshow('Mask', mask)
    cv2.imshow('Labeled Image', labels_im)
    cv2.waitKey(0)

cv2.destroyAllWindows()
