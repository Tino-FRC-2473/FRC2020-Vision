import serial
from pose_detector import PoseDetector
from video_live_generator import VideoLiveGenerator
from power_port_detector import PowerPortDetector


class DataSender:
    def __init__(self):
        name = "ttyTHS2"
        rate = 9600
        port = 1

        self.s = serial.Serial("/dev/" + name, rate)

        self.pose_detector = PoseDetector(PowerPortDetector(VideoLiveGenerator(port)))

    def convert_data(self):
        rot, trans = self.pose_detector.get_values()

        x = 0  # example:   296   cm      296
        y = 0  # example:  1324   cm     1324
        z = 0  # example: -  23.4 deg    -234

        return x, y, z

    def send_data(self):
        x, y, z = self.convert_data()
        self.s.write("S %04d %04d %.1s%04d E\n" % (x, y, "+" if z >= 0 else "-", abs(z)))  # example: S 0296 1324 -0234 E


data_sender = DataSender()

while True:
    data_sender.send_data()
