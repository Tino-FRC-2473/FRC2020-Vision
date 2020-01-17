import math
import cv2
import numpy as np
import subprocess
import imghdr
import random

class YellowCalibration:

    def __init__(self):

        rgb_data = np.loadtxt('yellow_data.csv', dtype=np.uint8, delimiter=',')
        bgr_data = np.copy(rgb_data)
        bgr_data[:, 0] = rgb_data[:, 2]
        bgr_data[:, 2] = rgb_data[:, 0]

        bgr_data = np.reshape(bgr_data, (401, 1, 3))

        self.TRUE_YELLOW_VALS = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)

        self.LOW_YELLOW = np.array([87, 3, 106])
        self.HIGH_YELLOW = np.array([103, 255, 255])



    def get_new_hsv(self, res):
        if (len(res) == 0):
        	return self.LOW_YELLOW, self.HIGH_YELLOW
        for i in range(100):
            row = random.randrange(0, len(res))
            self.TRUE_YELLOW_VALS = np.append(self.TRUE_YELLOW_VALS, np.reshape(np.array(res[row]), (1, 1, 3)), 0)

        h = self.TRUE_YELLOW_VALS[:, :, 0]
        s = self.TRUE_YELLOW_VALS[:, :, 1]
        v = self.TRUE_YELLOW_VALS[:, :, 2]
        low_h, low_s, low_v = (h.mean() - 1.25 * h.std()), (s.mean() - 2.5 * s.std()), (v.mean() - 2.25 * v.std())
        high_h, high_s, high_v = (h.mean() + 1.25 * h.std()), (s.mean() + 2.5 * s.std()), (v.mean() + 2.25 * v.std())
        return np.array([int(low_h), int(low_s), int(low_v)]), np.array([int(high_h), int(high_s), int(high_v)])

    def get_low_yellow():
        return self.LOW_YELLOW

    def get_high_yellow():
        return self.HIGH_YELLOW
