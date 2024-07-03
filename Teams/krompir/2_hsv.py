import cv2
import numpy as np
import os

# Function to update HSV values based on sliders
def update_hsv(dummy=None, image=None):
    global min_h, max_h, min_s, max_s, min_v, max_v
    min_h = cv2.getTrackbarPos('Min H', 'Mask Control')
    max_h = cv2.getTrackbarPos('Max H', 'Mask Control')
    min_s = cv2.getTrackbarPos('Min S', 'Mask Control')
    max_s = cv2.getTrackbarPos('Max S', 'Mask Control')
    min_v = cv2.getTrackbarPos('Min V', 'Mask Control')
    max_v = cv2.getTrackbarPos('Max V', 'Mask Control')

    # Apply HSV mask
    masked_image = apply_hsv_mask(image)
    cv2.imshow('HSV Masked Image', masked_image)

# Function to apply HSV mask
def apply_hsv_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([min_h, min_s, min_v])
    upper_bound = np.array([max_h, max_s, max_v])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

# Load an image
def main():
    # Initialize HSV range values (initial values)
    min_h, max_h = 0, 179
    min_s, max_s = 0, 255
    min_v, max_v = 0, 255

    # Create a window and sliders for HSV range adjustment
    cv2.namedWindow('Mask Control')
    cv2.resizeWindow('Mask Control', 400, 250)
    cv2.createTrackbar('Min H', 'Mask Control', min_h, 179, update_hsv)
    cv2.createTrackbar('Max H', 'Mask Control', max_h, 179, update_hsv)
    cv2.createTrackbar('Min S', 'Mask Control', min_s, 255, update_hsv)
    cv2.createTrackbar('Max S', 'Mask Control', max_s, 255, update_hsv)
    cv2.createTrackbar('Min V', 'Mask Control', min_v, 255, update_hsv)
    cv2.createTrackbar('Max V', 'Mask Control', max_v, 255, update_hsv)


    folder_path = './dataset/images/train/'
    for filename in os.listdir(folder_path):
        print(filename)
        # image_path = 'C:/Users/ante0/OneDrive/Desktop/ADOS_2024/Teams/korov_krompir/dataset/images/train/20240617_073726.jpg'
        image = cv2.imread(folder_path+filename)

        # Start the main loop
        while True:
            # Apply initial HSV mask
            masked_image = apply_hsv_mask(image)
            cv2.imshow('HSV Masked Image', masked_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Press 'q' to exit
                return
            elif key == ord('n'):
                break

    # Cleanup
    cv2.destroyAllWindows()


main()
