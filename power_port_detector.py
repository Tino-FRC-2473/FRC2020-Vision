import cv2
import numpy as np
from green_calibration import GreenCalibration
import matplotlib.pyplot as plt

class PowerPortDetector:

    # Constructor
    def __init__(self, generator):
        self.calibrator = GreenCalibration()
        self.input = generator

    # Runs the detector. This means that it'll actually detect the power port
    # and then it'll calibrate to the power port green color. This method returns
    # the contours of the actual power port.

    def run_detector(self):
        img, _ = self.input.generate()

        if img is None:
            return None, None

        img = cv2.GaussianBlur(img, (3, 3), cv2.BORDER_DEFAULT)
        luv = cv2.cvtColor(luv, cv2.COLOR_BGR2LUV)
        # plt.figure(figsize=(12, 6))
        # plt.subplot(1, 3, 1)
        # plt.title("Y")
        # plt.imshow(color[:,:,0])
        # plt.subplot(1, 3, 2)
        # plt.title("Cr")
        # plt.imshow(color[:,:,1])
        # plt.subplot(1, 3, 3)
        # plt.title("Cb")
        # plt.imshow(color[:,:,2])
        mask = cv2.inRange(luv, self.calibrator.low_green, self.calibrator.high_green)
        contours_return = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = None
        if len(contours_return) == 3:
            contours = contours_return[1]
        else:
            contours = contours_return[0]
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

        greens = luv[np.where((mask == 255))]

        self.calibrator.get_new_lab(greens)

        return contours, mask

    def get_generator(self):
        return self.input
