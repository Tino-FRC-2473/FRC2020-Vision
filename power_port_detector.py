import cv2
from green_calibration import GreenCalibration


class PowerPortDetector:
    # Constructor
    def __init__(self, generator):
        self.calibrator = GreenCalibration()
        self.input = generator

    # Runs the detector. This means that it'll actually detect the power port
    # and then it'll calibrate to the power port green color. This method returns
    # the contours of the actual power port.

    def run_detector(self):
        img = self.input.get_frame()
        img = cv2.GaussianBlur(img, (3, 3), cv2.BORDER_DEFAULT)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.calibrator.LOW_GREEN, self.calibrator.HIGH_GREEN)
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

        greens = hsv[np.where((mask == 255))]

        self.calibrator.get_new_hsv(greens)

        return contours

    def get_generator():
        return self.input
