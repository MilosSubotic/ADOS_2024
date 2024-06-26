import cv2
import os
from ultralytics import YOLO
import matplotlib.pyplot as plt


model = YOLO("C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/runs/detect/train6/weights/best.pt")

image_dir = "C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/dataset/images/test"


supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')


for filename in os.listdir(image_dir):
    if filename.lower().endswith(supported_extensions):
       
        image_path = os.path.join(image_dir, filename)
        image = cv2.imread(image_path)

        
        results = model(image)

       
        for result in results[0].boxes:  
            x1, y1, x2, y2 = result.xyxy[0]  
            conf = result.conf[0] 
            cls = result.cls[0]  
            label = model.names[int(cls)]  

            
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 3)

            
            cv2.putText(image, f"{label} {conf:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 3)

       
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        
        plt.imshow(image_rgb)
        plt.title(filename)
        plt.axis('off')
        plt.show()
