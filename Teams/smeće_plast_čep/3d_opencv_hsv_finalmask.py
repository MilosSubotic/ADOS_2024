import cv2
import numpy as np
import os
import glob

# Definisanje direktorijuma sa slikama
image_dir = '/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/images/test/'  # Putanja do direktorijuma sa slikama

# Pronađi sve slike u direktorijumu (jpg, png, itd.)
image_paths = glob.glob(os.path.join(image_dir, '*.*'))

# Definisanje HSV opsega za različite boje (crvena, zelena, plava)
color_ranges = {
    #lower - upper limit
    'black': ([0, 0, 0], [180, 255, 30]),
    'white': ([0, 0, 231], [180, 18, 255]),
    'red': ([159, 50, 70], [180, 255, 255]),
    'green': ([36, 50, 70], [89, 255, 255]),
    'blue': ([90, 50, 70], [128, 255, 255]),
    'yellow': ([25, 50, 70], [35, 255, 255]),
    'orange': ([10, 50, 70], [24, 255, 255])
}

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

        # Dodavanje oznaka na konačnu masku sa različitim vrednostima za svaku boju
        for i in range(1, num_labels):
            final_labels[labels_im == i] = label_count
            label_count += 1

    # Normalizacija etiketa za prikaz
    final_labels_normalized = cv2.normalize(final_labels, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Prikaz rezultata
    cv2.imshow('Original Image', image)
    cv2.imshow('Final Mask', final_labels_normalized)
    cv2.waitKey(0)  # Čeka na pritisak tastera da bi se prikazale sledeće slike

cv2.destroyAllWindows()
