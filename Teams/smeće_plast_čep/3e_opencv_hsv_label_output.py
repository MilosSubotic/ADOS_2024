import cv2
import numpy as np
import os
import glob

# Definisanje direktorijuma sa slikama
image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/images/test/'  # Putanja do direktorijuma sa slikama

# Putanja za čuvanje YOLO formata anotacija
annotation_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/labels/test'

# Kreiranje direktorijuma za YOLO anotacije ako ne postoji
os.makedirs(annotation_dir, exist_ok=True)

# Pronađi sve slike u direktorijumu (jpg, png, itd.)
image_paths = glob.glob(os.path.join(image_dir, '*.*'))

# Definisanje HSV opsega za različite boje (crvena, zelena, plava)
color_ranges = {
    'black': ([0, 0, 0], [180, 255, 45]),
    'white': ([0, 0, 240], [180, 111, 255]),
    'red': ([159, 50, 70], [180, 255, 255]),
    'green': ([36, 50, 70], [89, 255, 255]),
    'blue': ([90, 50, 70], [128, 255, 255]),
    'yellow': ([25, 50, 70], [35, 255, 255]),
    'orange': ([9, 100, 100], [29, 255, 255])
}

# Mapiranje klasa na YOLO indekse
class_map = {
    'black': 0,
    'white': 1,
    'red': 2,
    'green': 3,
    'blue': 4,
    'yellow': 5,
    'orange': 6
}

# Funkcija za čuvanje YOLO formata anotacija
def save_yolo_annotation(image_path, boxes):
    annotation_file = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
    with open(os.path.join(annotation_dir, annotation_file), 'w') as f:
        for box in boxes:
            class_idx = box[0]
            x_center = (box[1] + box[3]) / 2.0
            y_center = (box[2] + box[4]) / 2.0
            width = box[3] - box[1]
            height = box[4] - box[2]
            f.write(f"{class_idx} {x_center} {y_center} {width} {height}\n")

# Obrada svake slike iz direktorijuma
for image_path in image_paths:
    # Učitavanje slike
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image {image_path}")
        continue

    # Konverzija slike iz BGR u HSV prostor boja
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Inicijalizacija maske za konačni rezultat
    final_labels = np.zeros(hsv_image.shape[:2], dtype=np.int32)
    label_count = 1

    # Lista za čuvanje bounding box-ova
    boxes = []

    for color, (lower, upper) in color_ranges.items():
        # Kreiranje maske za trenutnu boju
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # Primena morfoloških operacija (dilatacija i erozija)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Etiketiranje objekata za trenutnu boju
        num_labels, labels_im = cv2.connectedComponents(mask)

        # Dodavanje bounding box-ova u listu
        for i in range(1, num_labels):
            points = np.argwhere(labels_im == i)
            x_min, y_min = points.min(axis=0)
            x_max, y_max = points.max(axis=0)
            boxes.append((class_map[color], x_min, y_min, x_max, y_max))

    # Čuvanje YOLO formata anotacija
    save_yolo_annotation(image_path, boxes)

    # Prikaz rezultata (opciono)
    # cv2.imshow('Original Image', image)
    # cv2.waitKey(0)

cv2.destroyAllWindows()
