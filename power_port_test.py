import cv2 as cv
from loading_bay_detector import LoadingBayDetector

vid = cv2.VideoCapture(1)
detector = LoadingBayDetector(None)

while(True):
    detector.run_detector(vid.read())
    cv2.waitKey(3)
