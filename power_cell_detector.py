import cv2
import numpy as np
# from depth_live_generator import DepthLiveGenerator


class PowerCellDetector:



    # Constructor
    def __init__(self, generator):
        self.input = generator
        self.LOW_YELLOW = np.array([17, 120, 120])
        self.HIGH_YELLOW = np.array([33, 255, 255])

    # Runs the detector. This means that it'll actually detect the loading bay
    # and then it'll calibrate to the loading bay green color. This method returns
    # the contours of the actual loading bay.

    def run_detector(self):
        img, _ = self.input.generate()

        if img is None:
            return None, None




        output = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv, 5)
        mask = cv2.inRange(hsv, self.LOW_YELLOW, self.HIGH_YELLOW)
        mask = cv2.erode(mask,None, iterations=7)
        mask = cv2.dilate(mask,None, iterations=10)

        output = cv2.bitwise_and(hsv, hsv, mask = mask)
        th2 = cv2.adaptiveThreshold(output[:,:,2], 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,10)

        circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 1.8, 40, param1=70, param2=50, minRadius=20, maxRadius=60)

        
        if(circles is None):
             return _, _

        detected_circles = np.uint16(np.around(circles))

        bottom_half_circles = []

        for (x, y ,r) in detected_circles[0, :]:
            # if(y < img.shape[0]/2):
            #      continue

            bottom_half_circles.append([x, y, r])
            #  cv2.circle(img, (x, y), r, (0, 0, 255), 3)
            #  cv2.circle(img, (x, y), 2, (255, 0, 0), 1)



        return bottom_half_circles, mask

    def get_generator(self):
        return self.input
