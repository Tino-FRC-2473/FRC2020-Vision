import cv2
import numpy as np
from depth_live_generator import DepthLiveGenerator
from video_live_generator import VideoLiveGenerator


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
            if key == ord('n'):
                self.update_floor("Press \'s\' to accept the depth frame and save as " + self.floor_destination + ".")
                return
            if key == ord('q'):
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
            if key == ord('q'):
                quit()

    def run_greens_test(self):
        pass

    def update_greens(self):
        pass

    def run_accuracy_test(self):
        pass

    def run_calibration(self):
        self.run_floor_test("Running floor test. Press \'y\' to accept the floor frame or \'n\' to update it.")
        # new_greens = self.run_greens_test()
        # print("New green values:", new_greens)
        # print(self.run_accuracy_test())
        # return new_greens
