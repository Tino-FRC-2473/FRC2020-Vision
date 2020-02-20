import cv2
from green_calibration import GreenCalibration


class PowerPortDetector:

    def __init__(self, generator):
        self.calibrator = GreenCalibration()
        self.input = generator

    def run_detector(self):
        img, _ = self.input.generate()

        if img is None:
            return None, None

        img = cv2.GaussianBlur(img, (3, 3), cv2.BORDER_DEFAULT)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.calibrator.low_green, self.calibrator.high_green)
        contours_return = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours_return) == 3:
            contours = contours_return[1]
        else:
            contours = contours_return[0]

        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

        self.calibrator.get_new_hsv(hsv, contours)
        return contours, mask

    def get_generator(self):
        return self.input
