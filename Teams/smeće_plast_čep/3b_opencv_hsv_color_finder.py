import numpy as np
import cv2

green = np.uint8([[[0, 165, 255]]]) # Here insert the BGR values which you want to convert to HSV
hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
print(hsvGreen)

lowerLimit = hsvGreen[0][0][0] - 10, 100, 100
upperLimit = hsvGreen[0][0][0] + 10, 255, 255

print(upperLimit)
print(lowerLimit)