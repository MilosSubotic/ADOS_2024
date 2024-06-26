import cv2
import os

# Function to annotate images with bounding boxes and save annotations in YOLO format
def annotate_images(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # List all image files in the input directory
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]
    
    print(f"Found {len(image_files)} images in {input_dir}")

    # Iterate through each image
    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        output_txt_path = os.path.join(output_dir, os.path.splitext(image_file)[0] + '.txt')
        
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image {image_path}")
            continue

        image_copy = image.copy()
        drawing = False
        ix, iy = -1, -1
        bbox_coordinates = []

        # Mouse callback function
        def draw_rectangle(event, x, y, flags, param):
            nonlocal ix, iy, drawing, image_copy, bbox_coordinates
            
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                ix, iy = x, y

            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing:
                    temp_image = image_copy.copy()
                    cv2.rectangle(temp_image, (ix, iy), (x, y), (0, 255, 0), 1)
                    cv2.imshow('image', temp_image)

            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                cv2.rectangle(image_copy, (ix, iy), (x, y), (0, 255, 0), 1)
                xmin = min(ix, x)
                xmax = max(ix, x)
                ymin = min(iy, y)
                ymax = max(iy, y)
                bbox_coordinates.append((xmin, ymin, xmax, ymax))
        
        # Display the image and annotate
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_rectangle)

        print(f"Annotating image {image_file}. Press 'q' to save and quit.")

        while True:
            cv2.imshow('image', image_copy)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
        
        # Save annotations to a text file in YOLO format
        with open(output_txt_path, 'w') as f:
            for bbox in bbox_coordinates:
                x_center = (bbox[0] + bbox[2]) / (2.0 * image.shape[1])
                y_center = (bbox[1] + bbox[3]) / (2.0 * image.shape[0])
                width = (bbox[2] - bbox[0]) / float(image.shape[1])
                height = (bbox[3] - bbox[1]) / float(image.shape[0])
                f.write(f'0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')  # Assuming class '0' for pothole
        
        cv2.destroyAllWindows()

if __name__ == '__main__':
    input_directory = r'C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\dataset\images'
    output_directory = r'C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\dataset\labels'
    annotate_images(input_directory, output_directory)
