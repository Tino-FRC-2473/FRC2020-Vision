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

        dx = trans[2]
        dy = trans[0]
        angle = rot[1]

        if trans[0] == -1.0 and rot[0] == 360.0:
            return 9999, 9999, 9999

        return int(100*dx), int(100*dy), 10*round(angle, 1)

    def send_data(self):
        x, y, z = self.convert_data()
        self.s.write("S %04d %04d %.1s%04d E\n" % (x, y, "+" if z >= 0 else "-", abs(z)))


data_sender = DataSender()

while True:
    data_sender.send_data()
