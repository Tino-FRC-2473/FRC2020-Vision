import cv2
import numpy as np
from green_calibration import GreenCalibration


calibrator = GreenCalibration()

while True:
    img = cv2.imread("test_photos/0degrees_18inches.png")
    img = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT) #blurs image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, calibrator.LOW_GREEN, calibrator.HIGH_GREEN)
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

    for contour in contours:
        epsilon = 0.1*cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,epsilon, True)
        print(approx)
        cv2.drawContours(img, approx, -1, (0, 0, 255), 3)


    greens = hsv[np.where((mask == 255))]

    calibrator.get_new_hsv(greens)
    cv2.imshow("img", img)
    cv2.imshow("mask", mask)

    cv2.waitKey(1)
