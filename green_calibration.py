import math
import cv2
import numpy as np
import subprocess
import imghdr
import random


class GreenCalibration:

    # This is how many standard deviations below and above the mean the low green/high green will be
    H_STD_TOLERANCE = 3.25
    S_STD_TOLERANCE = 3.5
    V_STD_TOLERANCE = 3.25

    def __init__(self, csv_data='green_data.csv'):

        rgb_data = np.loadtxt(csv_data, dtype=np.uint8, delimiter=',')
        bgr_data = np.copy(rgb_data)
        bgr_data[:, 0] = rgb_data[:, 2]
        bgr_data[:, 2] = rgb_data[:, 0]

        bgr_data = np.reshape(bgr_data, (79, 1, 3))

        self.true_green_vals = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)

        self.low_green = np.array([68, 100, 5])
        self.high_green = np.array([84, 255, 255])

    def get_new_hsv(self, mask):
        if (len(mask) == 0):
            return self.low_green, self.high_green
        for i in range(100):
            row = random.randrange(0, len(mask))
            self.true_green_vals = np.append(self.true_green_vals, np.reshape(np.array(mask[row]), (1, 1, 3)), 0)

        h = self.true_green_vals[:, :, 0]
        s = self.true_green_vals[:, :, 1]
        v = self.true_green_vals[:, :, 2]
        low_h, low_s, low_v = (h.mean() - self.H_STD_TOLERANCE * h.std()), (s.mean() - self.S_STD_TOLERANCE * s.std()), (v.mean() - self.V_STD_TOLERANCE * v.std())
        high_h, high_s, high_v = (h.mean() + self.H_STD_TOLERANCE * h.std()), (s.mean() + self.S_STD_TOLERANCE * s.std()), (v.mean() + self.V_STD_TOLERANCE * v.std())
        self.low_green = np.array([int(low_h), int(low_s), int(low_v)])
        self.high_green = np.array([int(high_h), int(high_s), int(high_v)])

    def get_low_green():
        return self.low_green

    def get_high_green():
        return self.high_green
