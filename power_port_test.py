import cv2 as cv
from loading_bay_detector import LoadingBayDetector

detector = LoadingBayDetector("video_live")

while(True):
    detector.run_detector()
    cv2.waitKey(3)
