import math
import argparse
import numpy as np
import serial
from depth_live_generator import DepthLiveGenerator
from pose_calculator import PoseCalculator
from power_cell_detector import PowerCellDetector
from power_port_detector import PowerPortDetector
from scipy.spatial.transform import Rotation as R
from video_live_generator import VideoLiveGenerator


class DataSender:

    def __init__(self, name="ttyS0", rate=9600, video_port=1, depth_port=2):
        self.s = serial.Serial("/dev/" + name, rate)
        self.pose_power_port = PoseCalculator(PowerPortDetector(VideoLiveGenerator(video_port)))
        self.pose_ball_detection = PoseCalculator(PowerCellDetector(DepthLiveGenerator(depth_port)))

    def get_power_port_data(self):
        rot, trans = self.pose_power_port.get_values()

        if trans[0] is None:
            return 9999, 9999, 9999

        dy = trans[0]
        dx = trans[2]
        angle = rot[1]

        return int(100 * dx), int(100 * dy), int(10 * round(angle, 1))

    def get_ball_detection_data(self):
        ball_data, obstacle_present = self.pose_ball_detection.get_balls()

        formatted = []
        for ball in ball_data:
            formatted.append([9999, 9999] if not ball else [int(100 * ball[0]), int(10 * round(ball[1], 1))])

        return formatted, obstacle_present

    def send_data(self):
        x, y, angle = self.get_power_port_data()
        data_to_send = "{:+05d} {:+05d} {:+05d} ".format(x, y, angle)

        balls, obstacle_present = self.get_ball_detection_data()
        data_to_send += " ".join("{:+05d} {:+05d}".format(ball[0], ball[1]) for ball in balls)
        data_to_send += " " + str(int(obstacle_present))

        self.s.write(bytes("S " + data_to_send + " E", "utf-8"))
        print("S " + data_to_send + " E")


parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", nargs="?", help="camera port to read from")
args = parser.parse_args()
data_sender = None

if args.port is not None:
    data_sender = DataSender(port=args.port)
else:
    data_sender = DataSender()

while True:
    data_sender.send_data()
