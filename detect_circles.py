import numpy as np
import cv2 as cv
img = cv.imread('test.jpg')
output = img.copy()
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
hsv = cv.medianBlur(hsv, 5)
cv.imshow("hsv", hsv[:,:,1])
circles = cv.HoughCircles(hsv[:,:,1], cv.HOUGH_GRADIENT, 0.5, 300, param1=50, param2=100, minRadius=0, maxRadius=0)
detected_circles = np.uint16(np.around(circles))
for (x, y ,r) in detected_circles[0, :]:
    cv.circle(output, (x, y), r, (0, 255, 0), 3)
    cv.circle(output, (x, y), 2, (255, 0, 0), 3)


cv.imshow('output',output)
cv.waitKey(0)
cv.destroyAllWindows()
