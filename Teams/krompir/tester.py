import cv2
import os
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Load the trained YOLO model
model = YOLO("C:/Users/ante0/OneDrive/Desktop/ADOS_2024/Teams/korov_krompir/runs/detect/train3/weights/best.pt")

# Directory containing images
image_dir = "C:/Users/ante0/OneDrive/Desktop/ADOS_2024/Teams/korov_krompir/dataset/images/test"

# Supported image file extensions
supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

# Loop through all files in the directory
for filename in os.listdir(image_dir):
    if filename.lower().endswith(supported_extensions):
        # Load an image
        image_path = os.path.join(image_dir, filename)
        image = cv2.imread(image_path)

        # Perform inference
        results = model(image)

        # Draw bounding boxes on the image
        for result in results[0].boxes:  # Loop through each box in the result
            x1, y1, x2, y2 = result.xyxy[0]  # Get bounding box coordinates
            conf = result.conf[0]  # Get confidence score
            cls = result.cls[0]  # Get class prediction
            label = model.names[int(cls)]  # Get label name

            # Draw rectangle
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 3)

            # Put label and confidence score
            cv2.putText(image, f"{label} {conf:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 3)

        # Convert BGR image to RGB for display
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the image
        plt.imshow(image_rgb)
        plt.title(filename)
        plt.axis('off')
        plt.show()