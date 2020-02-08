import cv2
import numpy as np
# from depth_live_generator import DepthLiveGenerator


class PowerCellDetector:

    # Constructor
    def __init__(self, generator):
        self.input = generator
        self.LOW_YELLOW = np.array([17, 120, 50])
        self.HIGH_YELLOW = np.array([33, 255, 255])

    # Runs the detector. This means that it'll actually detect the loading bay
    # and then it'll calibrate to the loading bay green color. This method returns
    # the contours of the actual loading bay.

    def run_detector(self):
        img, depth_frame = self.input.generate()

        if img is None:
            return None, None

        output = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv, 5)
        mask = cv2.inRange(hsv, self.LOW_YELLOW, self.HIGH_YELLOW)

        # erode removes white noise at edges of the contours.
        mask = cv2.erode(mask, None, iterations=7)

        # dilation increases the overall area of the object to accentuate the contours.
        mask = cv2.dilate(mask, None, iterations=10)

        # output = cv2.bitwise_and(hsv, hsv, mask=mask)
        # print(hsv[:,:,1])
        mask_copy = mask.copy()
        mask_copy[mask_copy > 1] = 1
        output = np.multiply(mask_copy, hsv[:, :, 2])
        # the two numbers at the end are the blockSize, which is basically how many pixels do we use to calculate the value of one of them
        # the last number is the number to subtract from the current weighted mean
        th2 = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10)
        circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 1.8, 40, param1=70, param2=50, minRadius=20, maxRadius=60)

        if(circles is None):
            return None, mask, depth_frame

        detected_circles = np.uint16(np.around(circles))
        print(detected_circles)

        circles = []

        for (x, y, r) in detected_circles[0, :]:
            # if(y < img.shape[0]/2):
            #      continue

            circles.append([x, y, r])
            #  cv2.circle(img, (x, y), r, (0, 0, 255), 3)
            #  cv2.circle(img, (x, y), 2, (255, 0, 0), 1)

        return circles, mask, depth_frame

    def get_generator(self):
        return self.input
