import cv2
import numpy as np
# from depth_live_generator import DepthLiveGenerator


class PowerCellDetector:

    # Constructor
    def __init__(self, generator):
        self.input = generator
        self.LOW_YELLOW = np.array([17, 120, 50])
        self.HIGH_YELLOW = np.array([33, 255, 255])

    # Runs the detector. This means that it'll detect power cells.
    # Returns in following format: (list of detected circles(with x-coordinate, y-coordinare, and radius)),
    # mask with detected circles,
    # color image,
    # depth frame
    def run_detector(self):
        img, depth_frame = self.input.generate()
        scale_percent = 1
        scaled_img = cv2.resize(img, (int(640*scale_percent), int(480*scale_percent)), interpolation=cv2.INTER_AREA)

        if img is None:
            return None, None

        output = scaled_img.copy()
        hsv = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv, 5)
        mask = cv2.inRange(hsv, self.LOW_YELLOW, self.HIGH_YELLOW)

        # erode removes white noise at edges of the contours.
        mask = cv2.erode(mask, None, iterations=7)

        # dilation increases the overall area of the object to accentuate the contours.
        mask = cv2.dilate(mask, None, iterations=10)

        # making a copy to make sure that the original mask is preserved when preparing for the adaptiveThreshold
        mask_copy = mask.copy()
        mask_copy[mask_copy > 1] = 1
        output = np.multiply(mask_copy, hsv[:, :, 1])

        # the two numbers at the end are the blockSize, which is basically how many pixels do we use to calculate the value of one of them
        # the last number is the number to subtract from the current weighted mean
        th2 = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10)
        th2 = ~th2

        circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 1.8, int(40*scale_percent), param1=int(70*scale_percent), param2=int(50*scale_percent), minRadius=int(20*scale_percent), maxRadius=int(60*scale_percent))

        if(circles is None):
            return None, mask, img, depth_frame

        detected_circles = np.uint16(np.around(circles))

        circles = []

        for (x, y, r) in detected_circles[0, :]:
            circles.append([x/scale_percent, y/scale_percent, r/scale_percent])

        return circles, mask, img, depth_frame

    def get_generator(self):
        return self.input
