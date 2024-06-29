import cv2
import numpy as np
import os

image_folder = '/home/stefan/Downloads/slike/images'

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append((filename, img))
    return images

# Load images
images = load_images_from_folder(image_folder)
if not images:
    print("No images found in the folder")
    exit(0)

current_image_index = 0

def update_mask(val):
    h_min = cv2.getTrackbarPos('H Min', 'HSV Mask')
    s_min = cv2.getTrackbarPos('S Min', 'HSV Mask')
    v_min = cv2.getTrackbarPos('V Min', 'HSV Mask')
    h_max = cv2.getTrackbarPos('H Max', 'HSV Mask')
    s_max = cv2.getTrackbarPos('S Max', 'HSV Mask')
    v_max = cv2.getTrackbarPos('V Max', 'HSV Mask')

    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])

    filename, img = images[current_image_index]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('HSV Mask', result)

cv2.namedWindow('HSV Mask')
cv2.createTrackbar('H Min', 'HSV Mask', 0, 179, update_mask)
cv2.createTrackbar('S Min', 'HSV Mask', 0, 255, update_mask)
cv2.createTrackbar('V Min', 'HSV Mask', 0, 255, update_mask)
cv2.createTrackbar('H Max', 'HSV Mask', 179, 179, update_mask)
cv2.createTrackbar('S Max', 'HSV Mask', 255, 255, update_mask)
cv2.createTrackbar('V Max', 'HSV Mask', 255, 255, update_mask)

def show_next_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(images)
    update_mask(0)

def show_previous_image():
    global current_image_index
    current_image_index = (current_image_index - 1) % len(images)
    update_mask(0)

update_mask(0)

# Main loop
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('n'):
        show_next_image()
    elif key == ord('b'):
        show_previous_image()
    elif key == 27:  # Escape key
        break

cv2.destroyAllWindows()
