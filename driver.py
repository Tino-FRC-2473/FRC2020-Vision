import cv2
from loading_bay_detector import LoadingBayDetector
from cv_color_calibration import GreenCalibration

img = cv2.imread("test_photos/0degrees_18inches.png")

detector = LoadingBayDetector(img)
calib = GreenCalibration()
while True:
    cv2.waitKey(1)
    detector.run_detector(img, calib)