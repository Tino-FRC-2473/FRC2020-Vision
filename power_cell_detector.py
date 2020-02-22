import cv2
import numpy as np
# from depth_live_generator import DepthLiveGenerator


class PowerCellDetector:

    # Constructor
    def __init__(self, generator):
        self.input = generator
        self.LOW_YELLOW = np.array([17, 120, 50])
        self.HIGH_YELLOW = np.array([33, 255, 255])

    # Returns in the following format:
    # list of detected circles (with x-coordinate, y-coordinate, and radius),
    # mask with detected circles,
    # color image,
    # depth frame
    def run_detector(self):
        img, depth_frame = self.input.generate()

        if img is None:
            return None, None

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv, 5)
        mask = cv2.inRange(hsv, self.LOW_YELLOW, self.HIGH_YELLOW)

        # Erode removes white noise at edges of the contours.
        mask = cv2.erode(mask, None, iterations=7)

        # Dilation increases the overall area of the object to accentuate the contours.
        mask = cv2.dilate(mask, None, iterations=10)

        # Making a copy to make sure that the original mask is preserved when preparing for the adaptiveThreshold
        mask_copy = mask.copy()
        mask_copy[mask_copy > 1] = 1
        output = np.multiply(mask_copy, hsv[:, :, 1])

        # The second-to-last parameter is the block size, which is the width of the square region to use to calculate
        # the threshold for a pixel--the threshold is different in different regions of the frame.
        th2 = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10)

        circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 1.8, 40, param1=70, param2=50, minRadius=20, maxRadius=60)
        if circles is None:
            return None, mask, img, depth_frame

        detected_circles = np.uint16(np.around(circles))
        circles = []
        for x, y, r in detected_circles[0, :]:
            circles.append([x, y, r])

        return circles, mask, img, depth_frame

    def get_generator(self):
        return self.input
