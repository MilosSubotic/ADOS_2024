import cv2
import numpy as np
import os


def nothing(x):
    pass


# Path to the image directory
image_dir = "datasets/weeds/train/images"

# Get list of images in the directory
image_files = [
    f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))
]
image_files.sort()
current_image_idx = 0

# Create a window
cv2.namedWindow("HSV Detector")

# Create trackbars for color change
cv2.createTrackbar("H Lower", "HSV Detector", 0, 179, nothing)
cv2.createTrackbar("S Lower", "HSV Detector", 0, 255, nothing)
cv2.createTrackbar("V Lower", "HSV Detector", 0, 255, nothing)
cv2.createTrackbar("H Upper", "HSV Detector", 179, 179, nothing)
cv2.createTrackbar("S Upper", "HSV Detector", 255, 255, nothing)
cv2.createTrackbar("V Upper", "HSV Detector", 255, 255, nothing)


# Function to adjust trackbar positions
def adjust_trackbar(trackbar_name, adjustment):
    current_value = cv2.getTrackbarPos(trackbar_name, "HSV Detector")
    new_value = current_value + adjustment
    max_value = 179 if "H" in trackbar_name else 255
    new_value = np.clip(new_value, 0, max_value)
    cv2.setTrackbarPos(trackbar_name, "HSV Detector", new_value)


while True:
    # Read the current image
    image_path = os.path.join(image_dir, image_files[current_image_idx])
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error loading image {image_path}")
        break

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get current positions of the trackbars
    h_lower = cv2.getTrackbarPos("H Lower", "HSV Detector")
    s_lower = cv2.getTrackbarPos("S Lower", "HSV Detector")
    v_lower = cv2.getTrackbarPos("V Lower", "HSV Detector")
    h_upper = cv2.getTrackbarPos("H Upper", "HSV Detector")
    s_upper = cv2.getTrackbarPos("S Upper", "HSV Detector")
    v_upper = cv2.getTrackbarPos("V Upper", "HSV Detector")

    # Define the HSV range
    lower_hsv = np.array([h_lower, s_lower, v_lower])
    upper_hsv = np.array([h_upper, s_upper, v_upper])

    # Create a mask based on the HSV range
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Perform bitwise AND between the frame and mask
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original frame and the result
    cv2.imshow("Original", frame)
    cv2.imshow("HSV Detector", result)

    # Check for keyboard inputs to switch images, adjust HSV values, or quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("n"):
        current_image_idx = (current_image_idx + 1) % len(image_files)
    elif key == ord("p"):
        current_image_idx = (current_image_idx - 1) % len(image_files)
    elif key == ord("i"):
        adjust_trackbar("H Lower", 1)
    elif key == ord("k"):
        adjust_trackbar("H Lower", -1)
    elif key == ord("o"):
        adjust_trackbar("S Lower", 1)
    elif key == ord("l"):
        adjust_trackbar("S Lower", -1)
    elif key == ord("u"):
        adjust_trackbar("V Lower", 1)
    elif key == ord("j"):
        adjust_trackbar("V Lower", -1)
    elif key == ord("y"):
        adjust_trackbar("H Upper", 1)
    elif key == ord("h"):
        adjust_trackbar("H Upper", -1)
    elif key == ord("t"):
        adjust_trackbar("S Upper", 1)
    elif key == ord("g"):
        adjust_trackbar("S Upper", -1)
    elif key == ord("r"):
        adjust_trackbar("V Upper", 1)
    elif key == ord("f"):
        adjust_trackbar("V Upper", -1)

# Close all windows
cv2.destroyAllWindows()
