import math
import argparse
import numpy as np
import serial
from pose_calculator import PoseCalculator
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:

    def __init__(self, name="ttyS0", rate=9600, port=0):
        self.s = serial.Serial("/dev/" + name, rate)
        self.pose_power_port = PoseCalculator(PowerPortDetector(VideoLiveGenerator(port)))

    def get_power_port_data(self):
        rot, trans = self.pose_power_port.get_values()

        if trans[0] is None:
            return 9999, 9999, 9999

        dy = trans[0]
        dx = trans[2]
        angle = -rot[1]

        return int(100 * dx), int(100 * dy), int(10 * round(angle, 1))

    def send_data(self):
        x, y, angle = self.get_power_port_data()
        data_to_send = "{:+05d} {:+05d} {:+05d} ".format(x, y, angle)

        self.s.write(bytes("S " + data_to_send + " E", "utf-8"))
        print("S " + data_to_send + " E")


parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", type=int, default=0, help="camera port to read from")
args = parser.parse_args()
data_sender = None

data_sender = DataSender(port=args.port)

while True:
    data_sender.send_data()
