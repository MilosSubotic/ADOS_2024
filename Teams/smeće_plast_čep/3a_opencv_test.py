import cv2 as cv
img = cv.imread('/home/stefziv/Documents/ADOS/ADOS_2024_FORK/Teams/smeće_plast_čep/dataset/images/test/IMG_20240618_131314784_result.jpg')

cv.imshow("Display window", img)
k = cv.waitKey(0) # Wait for a keystroke in the window