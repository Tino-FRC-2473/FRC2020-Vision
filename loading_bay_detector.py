import cv2
import numpy as np
from green_calibration import GreenCalibration
class LoadingBayDetector:

    # Constructor
    # int input_type(0-image, 1-video, 2-live-camera, 3-depth-image, 4-depth-video)
<<<<<<< HEAD
    def __init__(self, input_img):
        self.calibrator = GreenCalibration()
        inp = None
        if(input_type == 0):
            inp =
=======
    def __init__(self, input_img): 
        self.calibrator = GreenCalibration()
        inp = None
        if(input_type == 0):
            inp = 
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
        elif(input_type == 1):
            inp =
        elif(input_type == 2):
            inp =
        elif(input_type == 3):
            inp =
        else:
            inp =

    # Runs the detector, taking in the input image and calibrator object. This means that it'll actually
<<<<<<< HEAD
    # detect the loading bay and then it'll calibrate to the loading bay green color. This method returns
=======
    # detect the loading bay and then it'll calibrate to the loading bay green color. This method returns 
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
    # the contours of the actual loading bay.
    def run_detector(self, inp):
        img = inp
        img = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT) #blurs image
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.calibrator.LOW_GREEN, self.calibrator.HIGH_GREEN)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
<<<<<<< HEAD

=======
        
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
        greens = hsv[np.where((mask == 255))]

        self.calibrator.get_new_hsv(greens)

<<<<<<< HEAD
        cv2.imshow("frame", img)
        cv2.imshow("contours", contours)
        return contours
=======
        return contours
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
