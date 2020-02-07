import math
import cv2
import numpy as np
import subprocess
import imghdr
import traceback
import os
from math import sin, cos
from operator import add


# finds rotation and translation of vision targets
class CaptureImage:

    # initilaze variables
    def __init__(self, detector):

        self.detector = detector
        self.generator = detector.get_generator()

        frame, _ = self.generator.generate()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]
        
        # constant to scale down display windows
        self.DISPLAY_CONSTANT = 0.8 if self.SCREEN_HEIGHT > 1000 else 1.0


    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        cv2.destroyAllWindows()
        print("exited")

    def display_windows(self, frame, ref_frame):
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.namedWindow("ref_frame", cv2.WINDOW_NORMAL)

        cv2.resizeWindow("frame", (int(self.DISPLAY_CONSTANT * self.SCREEN_WIDTH), int(self.DISPLAY_CONSTANT * self.SCREEN_HEIGHT)))
        cv2.resizeWindow("ref_frame", (int(self.DISPLAY_CONSTANT * self.SCREEN_WIDTH), int(self.DISPLAY_CONSTANT * self.SCREEN_HEIGHT)))

        cv2.moveWindow("frame", 350, 30)
        cv2.moveWindow("ref_frame", 1000, 30)

        cv2.imshow("frame", frame)
        cv2.imshow("ref_frame", ref_frame)

    def update_frame(self):
        frame, _ = self.generator.generate()

        ref_frame, _ = self.generator.generate()
        cv2.circle(ref_frame, (int(self.SCREEN_WIDTH/2), int(self.SCREEN_HEIGHT/2 - 200)), 2, (255, 255, 255), 2)
        cv2.circle(ref_frame, (int(self.SCREEN_WIDTH/2), int(self.SCREEN_HEIGHT/2 + 200)), 2, (255, 255, 255), 2)

        self.display_windows(frame, ref_frame)

    def capture(self, dir_name, angle, distance):
        filename = dir_name + "/" + str(angle) + "degrees_" + str(distance) + "inches.png"
        frame, _ = self.generator.generate()
        cv2.imwrite(filename, frame)
