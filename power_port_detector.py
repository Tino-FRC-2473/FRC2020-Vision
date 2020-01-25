import cv2
from green_calibration import GreenCalibration
from video_live_generator import VideoLiveGenerator
# from depth_data_generator import DepthDataGenerator
# from video_file_generator import VideoFileGenrator
# from image_generator import ImageGenerator
# from depth_live_generator import DepthLiveGenerator

class PowerPortDetector:
    # Constructor
    def __init__(self, input_type):
        self.calibrator = GreenCalibration()
        self.inp = None
        if(input_type == "depth_data"):
            self.inp = DepthDataGenerator()
        elif(input_type == "depth_live"):
            self.inp = DepthLiveGenerator()
        elif(input_type == "image"):
            self.inp = ImageGenerator()
        elif(input_type == "video_file"):
            self.inp = VideoFileGenrator()
        elif(input_type == "video_live"):
            self.inp = VideoLiveGenerator(2)


    # Runs the detector, taking in the input image and calibrator object. This means that it'll actually
    # detect the power port and then it'll calibrate to the power port green color. This method returns
    # the contours of the actual power port.

    def run_detector(self):
        img = self.inp.get_frame()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.calibrator.LOW_GREEN, self.calibrator.HIGH_GREEN)
		_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

		greens = hsv[np.where((mask == 255))]

        self.calibrator.get_new_hsv(greens)

        return contours
