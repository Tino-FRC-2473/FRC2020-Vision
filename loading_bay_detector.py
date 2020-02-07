import cv2
import numpy as np
from green_calibration import GreenCalibration


class LoadingBayDetector:

    # Constructor
    def __init__(self, generator):
        self.calibrator = GreenCalibration()
        self.input = generator

    # Runs the detector. This means that it'll actually detect the power port
    # and then it'll calibrate to the loading bay green color. This method returns
    # the contours of the actual loading bay.

    def run_detector(self):
        img, _ = self.input.generate()
        img = cv2.GaussianBlur(img, (7, 7), cv2.BORDER_DEFAULT)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, self.calibrator.low_green, self.calibrator.high_green)
        contours_return = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = None
        if len(contours_return) == 3:
            contours = contours_return[1]
        else:
            contours = contours_return[0]

        final_contours = []

        for c in contours:
            if(cv2.contourArea(c) > 50):
                final_contours.append(c)
        final_contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

        greens = hsv[np.where((mask == 255))]

        self.calibrator.get_new_hsv(greens)
        cv2.imshow("mask", mask)
        return final_contours

    def get_generator():
        return self.input
