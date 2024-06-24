import cv2
import numpy as np
import yaml
import os

# Function to read configuration file
def read_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['classes']

# Function to process images
def process_images(input_dir, output_dir, classes):
    # Process each image in the input directory
    subdirs = os.listdir(input_dir)
    for subdir in subdirs:
        sub_input_dir = os.path.join(input_dir, subdir)
        sub_output_dir = os.path.join(output_dir, subdir)
        contours_dir = os.path.join('./dataset/contours', subdir)
        
        os.makedirs(sub_output_dir, exist_ok=True)  # Create subdirectory in output_dir if not exists
        os.makedirs(contours_dir, exist_ok=True)    # Create subdirectory in contours if not exists

        # Process each image file in the subdirectory
        for image_name in os.listdir(sub_input_dir):
            if image_name.endswith(('.jpg', '.jpeg', '.png')):
                # Read the image
                image_path = os.path.join(sub_input_dir, image_name)
                image = cv2.imread(image_path)
                if image is None:
                    continue
                image_height, image_width, _ = image.shape

                # Convert the image to HSV color space
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # List to store all bounding boxes for detected objects
                all_bounding_boxes = []

                # Process each class defined in the configuration
                for class_config in classes:
                    # Define HSV range for the current class
                    h_start = class_config['H']['start']
                    h_stop = class_config['H']['stop']
                    s_start = class_config['S']['start']
                    s_stop = class_config['S']['stop']
                    v_start = class_config['V']['start']
                    v_stop = class_config['V']['stop']

                    # Handle the hue range
                    if h_start > h_stop:
                        lower_mask1 = cv2.inRange(hsv_image, 
                                                  np.array([h_start, s_start, v_start]),
                                                  np.array([180, s_stop, v_stop]))
                        lower_mask2 = cv2.inRange(hsv_image, 
                                                  np.array([0, s_start, v_start]),
                                                  np.array([h_stop, s_stop, v_stop]))
                        mask = cv2.bitwise_or(lower_mask1, lower_mask2)
                    else:
                        mask = cv2.inRange(hsv_image, 
                                           np.array([h_start, s_start, v_start]),
                                           np.array([h_stop, s_stop, v_stop]))

                    # Find contours in the mask
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    # Process each contour for the current class
                    for contour in contours:
                        # Filter contours based on area
                        area = cv2.contourArea(contour)
                        if area < 2500:
                            continue

                        # Get bounding box coordinates
                        x, y, w, h = cv2.boundingRect(contour)

                        # Calculate normalized coordinates
                        x_center = (x + w / 2) / image_width
                        y_center = (y + h / 2) / image_height
                        width = w / image_width
                        height = h / image_height

                        # Store bounding box information
                        all_bounding_boxes.append((class_config['class_id'], x_center, y_center, width, height))

                        # Draw rectangle on the original image for visualization
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Export images with contour for debug
                output_image_path = os.path.join(contours_dir, image_name)
                cv2.imwrite(output_image_path, image)

                # Prepare output file
                output_file_path = os.path.join(sub_output_dir, os.path.splitext(image_name)[0] + '.txt')

                # Write data
                with open(output_file_path, 'w') as file:
                    for bbox_info in all_bounding_boxes:
                        class_id, x_center, y_center, width, height = bbox_info
                        file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

                # Write classes.txt file for the current subdirectory
                classes_txt_path = os.path.join(sub_output_dir, 'classes.txt')

                with open(classes_txt_path, 'w') as file:
                    for class_config in classes:
                        class_name = class_config['class_name']
                        file.write(f"{class_name}\n")

    print("Labeling complete.")

# Read configuration file
config_file = './cfg/HSV_Thresholds.cfg.yaml'
classes = read_config(config_file)

# Input and output directories
input_dir = './dataset/images'
output_dir = './dataset/labels'

# Process images in subdirectories of input_dir
process_images(input_dir, output_dir, classes)
