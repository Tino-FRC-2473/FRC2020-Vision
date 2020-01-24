import math
import cv2
import numpy as np
import subprocess
import imghdr
import random

class GreenCalibration:

    def __init__(self):
<<<<<<< HEAD

=======
        
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
        rgb_data = np.loadtxt('green_data.csv', dtype=np.uint8, delimiter=',')
        bgr_data = np.copy(rgb_data)
        bgr_data[:, 0] = rgb_data[:, 2]
        bgr_data[:, 2] = rgb_data[:, 0]
<<<<<<< HEAD

        bgr_data = np.reshape(bgr_data, (79, 1, 3))

        self.TRUE_GREEN_VALS = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)

=======
        
        bgr_data = np.reshape(bgr_data, (79, 1, 3))

        self.TRUE_GREEN_VALS = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)
        
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
        self.LOW_GREEN = np.array([68, 100, 50])
        self.HIGH_GREEN = np.array([84, 255, 255])



    def get_new_hsv(self, res):
        if (len(res) == 0):
        	return self.LOW_GREEN, self.HIGH_GREEN
        for i in range(100):
            row = random.randrange(0, len(res))
            self.TRUE_GREEN_VALS = np.append(self.TRUE_GREEN_VALS, np.reshape(np.array(res[row]), (1, 1, 3)), 0)
<<<<<<< HEAD

=======
        
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
        h = self.TRUE_GREEN_VALS[:, :, 0]
        s = self.TRUE_GREEN_VALS[:, :, 1]
        v = self.TRUE_GREEN_VALS[:, :, 2]
        low_h, low_s, low_v = (h.mean() - 3.25 * h.std()), (s.mean() - 3.5 * s.std()), (v.mean() - 3.25 * v.std())
        high_h, high_s, high_v = (h.mean() + 3.25 * h.std()), (s.mean() + 3.5 * s.std()), (v.mean() + 3.25 * v.std())
<<<<<<< HEAD
        self.LOW_GREEN = np.array([int(low_h), int(low_s), int(low_v)])
        self.HIGH_GREEN = np.array([int(high_h), int(high_s), int(high_v)])

    def get_low_green():
        return self.LOW_GREEN

    def get_high_green():
        return self.HIGH_GREEN
=======
        return np.array([int(low_h), int(low_s), int(low_v)]), np.array([int(high_h), int(high_s), int(high_v)])

    def get_low_green():
        return self.LOW_GREEN
    
    def get_high_green():
        return self.HIGH_GREEN
    
>>>>>>> 33284ee83d4fb08152c0c8b1cab86b9aecf76346
