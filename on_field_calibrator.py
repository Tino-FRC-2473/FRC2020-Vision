import argparse
import cv2
import numpy as np
import random
from depth_live_generator import DepthLiveGenerator
from power_cell_detector import PowerCellDetector
from video_live_generator import VideoLiveGenerator


class OnFieldCalibrator:
    def __init__(self, video_port=1, depth_port=2, floor_path="FLOOR.csv", greens_path="green_data1.csv"):
        self.video_generator = VideoLiveGenerator(video_port)
        self.depth_generator = DepthLiveGenerator(depth_port)

        self.floor_path = floor_path
        self.greens_path = greens_path
        self.floor_frame = np.loadtxt(floor_path, dtype=np.float32, delimiter=",")
        self.floor_frame[self.floor_frame > 4] = 0

    def run_floor_test(self):
        print("Running floor test. Press \'y\' to accept the floor frame or \'n\' to update it.")
        print("Press \'q\' to quit.")

        while True:
            _, depth = self.depth_generator.generate()
            subtracted = np.where(abs(depth - self.floor_frame) < 0.05, 0, depth)
            cv2.imshow("Floor frame", self.floor_frame)
            cv2.imshow("Without floor", subtracted)

            key = cv2.waitKey(1)
            if key == ord("y"):
                cv2.destroyAllWindows()
                return
            elif key == ord("n"):
                cv2.destroyAllWindows()
                self.update_floor()
                print("Press \'y\' to accept the floor frame or \'n\' to update it again.")
            elif key == ord("q"):
                quit()

    def update_floor(self):
        print("Press \'s\' to accept the depth frame and save as " + self.floor_path + ".")
        print("Press \'q\' to quit.")

        while True:
            _, depth = self.depth_generator.generate()
            cv2.imshow("Depth frame", depth)

            key = cv2.waitKey(1)
            if key == ord("s"):
                np.savetxt(self.floor_path, depth, delimiter=",", fmt="%s")
                self.floor_frame = depth
                self.floor_frame[self.floor_frame > 4] = 0
                cv2.destroyAllWindows()
                return
            elif key == ord("q"):
                quit()

    def update_greens(self):
        print("Running green calibration test. Press \'r\' to accept green values or \'p\' to print them.")
        print("Press \'q\' to quit.")

        cv2.namedWindow("Calibrations")

        cv2.createTrackbar("H low", "Calibrations", 68, 255, lambda x: None)
        cv2.createTrackbar("S low", "Calibrations", 100, 255, lambda x: None)
        cv2.createTrackbar("V low", "Calibrations", 50, 255, lambda x: None)

        cv2.createTrackbar("H high", "Calibrations", 84, 255, lambda x: None)
        cv2.createTrackbar("S high", "Calibrations", 255, 255, lambda x: None)
        cv2.createTrackbar("V high", "Calibrations", 255, 255, lambda x: None)

        while True:
            frame, _ = self.video_generator.generate()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            hl = cv2.getTrackbarPos("H low", "Calibrations")
            sl = cv2.getTrackbarPos("S low", "Calibrations")
            vl = cv2.getTrackbarPos("V low", "Calibrations")

            hh = cv2.getTrackbarPos("H high", "Calibrations")
            sh = cv2.getTrackbarPos("S high", "Calibrations")
            vh = cv2.getTrackbarPos("V high", "Calibrations")

            low_green = np.array([hl, sl, vl])
            high_green = np.array([hh, sh, vh])

            mask = cv2.inRange(hsv, low_green, high_green)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            both = np.hstack((frame, mask))
            cv2.imshow("Calibrations", both)

            key = cv2.waitKey(1)
            if key == ord("r"):
                cv2.destroyAllWindows()
                return low_green, high_green
            elif key == ord("p"):
                print("low:", low_green)
                print("high:", high_green, "\n")
            elif key == ord("q"):
                quit()

    def update_green_csv(self, low_green, high_green):
        img, _ = self.video_generator.generate()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, low_green, high_green)
        greens = img[np.where(mask == 255)]

        with open(self.greens_path, "w") as file:
            for i in range(100):
                row = random.randrange(0, len(greens))
                rgb = np.flip(greens[row])
                file.write(",".join(map(str, rgb)) + "\n")

    def run_ball_test(self):
        print("Running balls test. Press \'c\' to continue.")
        print("Press \'q\' to quit.")
        power_cell_detector = PowerCellDetector(self.depth_generator)

        while True:
            circles, depth_frame = power_cell_detector.run_detector()
            for circle in circles:
                if circle is not None:
                    cv2.circle(depth_frame, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 0, 255), 3)
                    cv2.circle(depth_frame, (int(circle[0]), int(circle[1])), 0, (255, 0, 0), 6)

            cv2.imshow("Depth frame with balls", depth_frame * 0.4)

            key = cv2.waitKey(1)
            if key == ord("c"):
                cv2.destroyAllWindows()
                return
            elif key == ord("q"):
                quit()

    def run_calibration(self):
        self.run_floor_test()
        low_green, high_green = self.update_greens()
        self.update_green_csv(low_green, high_green)
        self.run_ball_test()
        print("Calibration complete.")


parser = argparse.ArgumentParser()
parser.add_argument("--video_port", "-v", type=int, default=1, help="camera port to read for VideoLiveGenerator")
parser.add_argument("--depth_port", "-d", type=int, default=2, help="camera port to read for DepthLiveGenerator")
parser.add_argument("--floor_path", "-f", type=str, default="FLOOR.csv", help="path of floor data CSV file")
parser.add_argument("--greens_path", "-g", type=str, default="green_data1.csv", help="path of green data CSV file")
args = parser.parse_args()

on_field_calibrator = OnFieldCalibrator(args.video_port, args.depth_port, args.floor_path, args.greens_path)
on_field_calibrator.run_calibration()
