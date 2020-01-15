import cv2
from cv_color_calibration import GreenCalibration
class PowerPortDetector:

    # Constructor
    # int input_type(0-image, 1-video, 2-live-camera, 3-depth-image, 4-depth-video)
    def __init__(self, input_type): 
        calib = GreenCalibration()
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

        run_detector(inp, calib)

    # Runs the detector, taking in the input image and calibrator object. This means that it'll actually
    # detect the power port and then it'll calibrate to the power port green color. This method returns 
    # the contours of the actual power port.

    def run_detector(self, inp, calibrator):
        img = input_feed;
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, calibrator.LOW_GREEN, calibrator.HIGH_GREEN)
		_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

		greens = hsv[np.where((mask == 255))]

        calibrator.get_new_hsv(greens)

        return contours