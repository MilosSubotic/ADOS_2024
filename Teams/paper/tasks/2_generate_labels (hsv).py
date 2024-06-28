import cv2  #OpenCV
import numpy as np
import yaml
import os

MIN_AREA_THRESHOLD = 2500


def read_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['classes']

def process_images(input_dir, output_dir, classes):
    # List subdirectories
    subdirs = os.listdir(input_dir)  # subdirs = [test, train, val]

    # Proccess each subdirectory
    for subdir in subdirs:
        sub_input_dir = os.path.join(input_dir, subdir)            # images/ + subdir
        sub_output_dir = os.path.join(output_dir, subdir)          # labels/ + subdir
        contours_dir = os.path.join('./dataset/contours', subdir)  # countours/ + subdir
        
        os.makedirs(sub_output_dir, exist_ok=True)  # Create subdirectory in output_dir if not exists
        os.makedirs(contours_dir, exist_ok=True)    # Create subdirectory in contours if not exists

        # Process each image in the subdirectory
        for image_name in os.listdir(sub_input_dir):
            if image_name.endswith(('.jpg', '.jpeg', '.png')):
                # Read image
                image_path = os.path.join(sub_input_dir, image_name)
                image = cv2.imread(image_path)
                if image is None:
                    continue

                # Extract image dimensions
                image_height, image_width, _ = image.shape  

                # Convert image to HSV color space
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # List to store all bounding boxes
                all_bounding_boxes = []

                # Process each class defined in the configuration
                for class_config in classes:

                    # Define HSV range for current class
                    h_start = class_config['H']['start']
                    h_stop = class_config['H']['stop']

                    s_start = class_config['S']['start']
                    s_stop = class_config['S']['stop']

                    v_start = class_config['V']['start']
                    v_stop = class_config['V']['stop']

                    # Mask image with HSV range
                    mask = cv2.inRange(hsv_image, 
                                           np.array([h_start, s_start, v_start]),
                                           np.array([h_stop, s_stop, v_stop]))

                    # Detect contours in masked image
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    # Process each contour for current class
                    for contour in contours:
                        # Filter contours based on area
                        area = cv2.contourArea(contour)
                        if area < MIN_AREA_THRESHOLD:  # Filter small, irrelevant objects
                            continue

                        # Get bounding box coordinates
                        x, y, w, h = cv2.boundingRect(contour)

                        # Calculate normalized coordinates (scale to [0,1] range)
                        x_center = (x + w / 2) / image_width
                        y_center = (y + h / 2) / image_height
                        width = w / image_width
                        height = h / image_height

                        # Store bounding box coordinates
                        all_bounding_boxes.append((class_config['class_id'], x_center, y_center, width, height))

                        # Draw rectangle(bounding box) on image for visualization
                        cv2.rectangle(image, (x, y), (x + w, y + h), class_config['bb_color'], 2)
                
                # Export current image with bounding boxes for debug
                output_image_path = os.path.join(contours_dir, image_name)
                cv2.imwrite(output_image_path, image)
				
                # Write labels for current image
                output_file_path = os.path.join(sub_output_dir, os.path.splitext(image_name)[0] + '.txt')
                with open(output_file_path, 'w') as file:
                    for bbox_info in all_bounding_boxes:
                        class_id, x_center, y_center, width, height = bbox_info
                        file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

        # Write classes.txt file for current subdirectory
        classes_txt_path = os.path.join(sub_output_dir, 'classes.txt')
        with open(classes_txt_path, 'w') as file:
            for class_config in classes:
                class_name = class_config['class_name']
                file.write(f"{class_name}\n")

    print("Labeling complete.")


# Read HSV configuration
config_file = './cfg/HSV_Thresholds.cfg.yaml'
classes = read_config(config_file)

# Set paths
input_dir = './dataset/images'
output_dir = './dataset/labels'

# Do labeling
process_images(input_dir, output_dir, classes)