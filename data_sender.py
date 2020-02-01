import math
import serial
from pose_calculator import PoseCalculator
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:
    def __init__(self):
        name = "ttyTHS2"
        rate = 9600
        port = 1

        self.s = serial.Serial("/dev/" + name, rate)

        self.pose_calculator = PoseCalculator(PowerPortDetector(VideoLiveGenerator(port)))

    def convert_data(self):
        rot, trans = self.pose_calculator.get_values()

        camera_tilt = trans[2]

        dx = abs(trans[2] * math.cos(camera_tilt)) * 2.54
        dy = abs(trans[0]) * 2.54
        angle = rot[1]

        if trans[0] is None:
            return 9999, 9999, 9999

        return int(100 * dx), int(100 * dy), 10 * round(angle, 1)

    def send_data(self):
        x, y, z = self.convert_data()
        self.s.write("S %04d %04d %.1s%04d E\n" % (x, y, "+" if z >= 0 else "-", abs(z)))


data_sender = DataSender()

while True:
    data_sender.send_data()
