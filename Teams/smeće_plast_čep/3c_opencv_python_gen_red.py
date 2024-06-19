import cv2
import numpy as np

# Učitavanje slike
image = cv2.imread('/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/images/test/IMG_20240618_131314784_result.jpg')

# Konverzija slike iz BGR u HSV prostor boja
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definisanje HSV opsega za ciljne boje (primer za crvenu boju)
lower_red = np.array([9, 100, 100])
upper_red = np.array([29, 255, 255])

# Kreiranje maske za crvenu boju
mask = cv2.inRange(hsv_image, lower_red, upper_red)

# Primena morfoloških operacija (dilatacija i erozija)
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Etiketiranje objekata
num_labels, labels_im = cv2.connectedComponents(mask)

# Normalizacija etiketa za prikaz
labels_im = cv2.normalize(labels_im, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Prikaz rezultata
cv2.imshow('Original Image', image)
cv2.imshow('Mask', mask)
cv2.imshow('Labeled Image', labels_im)
cv2.waitKey(0)
cv2.destroyAllWindows()
