import cv2
import numpy as np
import os
import glob

# Define the directory with images
image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/images/train/'  # Path to the directory with images

# Path to save YOLO format annotations
annotation_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/labels/train'

# Create the directory for YOLO annotations if it doesn't exist
os.makedirs(annotation_dir, exist_ok=True)

# Find all images in the directory (jpg, png, etc.)
image_paths = glob.glob(os.path.join(image_dir, '*.*'))

# Define HSV ranges for different colors (red, green, blue, etc.)
color_ranges = {
    'black': ([0, 0, 0], [180, 255, 45]),
    'white': ([0, 0, 240], [180, 111, 255]),
    'red': ([159, 50, 70], [180, 255, 255]),
    'green': ([36, 50, 70], [89, 255, 255]),
    'blue': ([90, 50, 70], [128, 255, 255]),
    'yellow': ([25, 50, 70], [35, 255, 255]),
    'orange': ([9, 100, 100], [29, 255, 255])
}

# Map classes to YOLO indices
class_map = {
    'black': 0,
    'white': 1,
    'red': 2,
    'green': 3,
    'blue': 4,
    'yellow': 5,
    'orange': 6
}

# Function to save YOLO format annotations
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

# Process each image in the directory
for image_path in image_paths:
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image {image_path}")
        continue

    # Get image dimensions
    image_height, image_width = image.shape[:2]

    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initialize mask for final result
    final_labels = np.zeros(hsv_image.shape[:2], dtype=np.int32)
    label_count = 1

    # List to store bounding boxes
    boxes = []

    for color, (lower, upper) in color_ranges.items():
        # Create a mask for the current color
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # Apply morphological operations (dilation and erosion)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Label objects for the current color
        num_labels, labels_im = cv2.connectedComponents(mask)

        # Add bounding boxes to the list
        for i in range(1, num_labels):
            points = np.argwhere(labels_im == i)
            x_min, y_min = points.min(axis=0)
            x_max, y_max = points.max(axis=0)
            boxes.append((class_map[color], x_min, y_min, x_max, y_max))

    # Save YOLO format annotations
    save_yolo_annotation(image_path, boxes, image_width, image_height)

    # Display the result (optional)
    # cv2.imshow('Original Image', image)
    # cv2.waitKey(0)

cv2.destroyAllWindows()
