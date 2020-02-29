import cv2
import numpy as np
from depth_live_generator import DepthLiveGenerator
from video_live_generator import VideoLiveGenerator
import random


class OnFieldCalibration:
    def __init__(self, video_port, depth_port, floor_destination):
        self.video_generator = VideoLiveGenerator(video_port)
        self.depth_generator = DepthLiveGenerator(depth_port)

        self.floor_destination = floor_destination
        self.floor_frame = np.loadtxt(floor_destination, dtype=np.float32, delimiter=",")
        self.floor_frame[self.floor_frame > 4] = 0

    def run_floor_test(self, prompt):
        print(prompt)
        print("Press \'q\' to quit.")

        while True:
            _, depth = self.depth_generator.generate()
            subtracted = np.where(abs(depth - self.floor_frame) < 0.05, 0, depth)
            cv2.imshow("Floor frame", self.floor_frame)
            cv2.imshow("Without floor", subtracted)

            key = cv2.waitKey(1)
            if key == ord('y'):
                return
            elif key == ord('n'):
                self.update_floor("Press \'s\' to accept the depth frame and save as " + self.floor_destination + ".")
                return
            elif key == ord('q'):
                quit()

    def update_floor(self, prompt):
        print(prompt)
        print("Press \'q\' to quit.")

        while True:
            _, depth = self.depth_generator.generate()
            cv2.imshow("Depth frame", depth)

            key = cv2.waitKey(1)
            if key == ord('s'):
                np.savetxt(self.floor_destination, depth, delimiter=",", fmt="%s")
                self.floor_frame = depth
                self.floor_frame[self.floor_frame > 4] = 0
                return
            elif key == ord('q'):
                quit()

    def run_greens_test(self):
        pass

    def update_greens(self):
        def nothing(x):
            pass

        cv2.createTrackbar("H-L", "Calibrations", 60, 255, nothing)
        cv2.createTrackbar("H-H", "Calibrations", 87, 255, nothing)
        cv2.createTrackbar("S-L", "Calibrations", 90, 255, nothing)
        cv2.createTrackbar("S-H", "Calibrations", 255, 255, nothing)
        cv2.createTrackbar("V-L", "Calibrations", 50, 255, nothing)
        cv2.createTrackbar("V-H", "Calibrations", 229, 255, nothing)

        while True:
            frame, _ = self.video_generator.generate()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            hl = cv2.getTrackbarPos("H-L", "Calibrations")
            hh = cv2.getTrackbarPos("H-H", "Calibrations")
            sl = cv2.getTrackbarPos("S-L", "Calibrations")
            sh = cv2.getTrackbarPos("S-H", "Calibrations")
            vl = cv2.getTrackbarPos("V-L", "Calibrations")
            vh = cv2.getTrackbarPos("V-H", "Calibrations")

            low_green = np.array([hl, sl, vl])
            high_green = np.array([hh, sh, vh])
            mask = cv2.inRange(hsv, low_green, high_green)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            both = np.hstack((frame, mask))

            cv2.imshow('Calibrations', both)

            key = cv2.waitKey(1)
            if key == ord('q'):
                return low_green, high_green
            elif key == ord('w'):
                print('low: [' + str(hl) + ', ' + str(sl) + ', ' + str(vl) + ']')
                print('high: [' + str(hh) + ', ' + str(sh) + ', ' + str(vh) + ']')
                print('------------------')

    def run_accuracy_test(self):
        pass

    def run_calibration(self):
        self.run_floor_test("Running floor test. Press \'y\' to accept the floor frame or \'n\' to update it.")

        low_green, high_green = self.update_greens()
        img, _ = self.video_generator.generate()
        mask = cv2.inRange(img, low_green, high_green)
        greens = img[np.where((mask[:, :, 0] == 255))]
        fout = open("green_data.csv","w")
        for i in range(100):
            row = random.randrange(0, len(greens))
            fout.write(np.reshape(np.array(greens[row]), (1, 1, 3)), 0)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        
        print('Calibration complete!')



        # new_greens = self.run_greens_test()
        # print("New green values:", new_greens)
        # print(self.run_accuracy_test())
        # return new_greens
