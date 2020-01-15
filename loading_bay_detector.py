import cv2
import numpy as np
from cv_color_calibration import GreenCalibration
class LoadingBayDetector:

    # Constructor
    # int input_type(0-image, 1-video, 2-live-camera, 3-depth-image, 4-depth-video)
    def __init__(self, input_img): 
        inp = None
        if(input_type == 0):
            inp = 
        elif(input_type == 1):
            inp =
        elif(input_type == 2):
            inp =
        elif(input_type == 3):
            inp =
        else:
            inp =

    # Runs the detector, taking in the input image and calibrator object. This means that it'll actually
    # detect the loading bay and then it'll calibrate to the loading bay green color. This method returns 
    # the contours of the actual loading bay.
    def run_detector(self, inp, calibrator):
        img = inp
        img = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT) #blurs image
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, calibrator.LOW_GREEN, calibrator.HIGH_GREEN)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
        
        greens = hsv[np.where((mask == 255))]

        calibrator.get_new_hsv(greens)

        cv2.imshow("img", img)
        cv2.imshow("mask", mask)

        return contours