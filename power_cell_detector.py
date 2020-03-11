import cv2
import numpy as np


class PowerCellDetector:
    def __init__(self, generator):
        self.input = generator
        self.LOW_YELLOW = np.array([17, 120, 50])
        self.HIGH_YELLOW = np.array([33, 255, 255])

    # Returns a tuple with:
    # - a list of detected circles, each with [x-coordinate, y-coordinate, radius].
    # - the depth frame
    def run_detector(self):
        img, depth_frame = self.input.generate()

        if img is None:
            return None, None

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOW_YELLOW, self.HIGH_YELLOW)
        mask = cv2.medianBlur(mask, 5)

        # Erode removes white noise at edges of the contours.
        mask = cv2.erode(mask, None, iterations=7)

        # Dilation increases the overall area of the object to accentuate the contours.
        mask = cv2.dilate(mask, None, iterations=10)
        output = (mask == 255) * hsv[:, :, 1]

        # The second-to-last parameter is the block size, which is the width of the square region to use to calculate
        # the threshold for a pixel--the threshold is different in different regions of the frame.
        th = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10)
        circles = cv2.HoughCircles(th, cv2.HOUGH_GRADIENT, 1.8, 40, param1=70, param2=50, minRadius=20, maxRadius=60)
        if circles is None:
            return None, depth_frame

        detected_circles = np.uint16(np.around(circles))
        circles = []
        for x, y, r in detected_circles[0, :]:
            if mask[y, x] != 0:
                circles.append([x, y, r])
    
        return circles, depth_frame

    def get_generator(self):
        return self.input
