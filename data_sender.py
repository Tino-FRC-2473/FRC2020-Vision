import math
import serial
from pose_calculator import PoseCalculator
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:
    CAMERA_TILT = 9999
    def __init__(self):
        name = "ttyTHS2"
        rate = 9600
        port = 1

        self.s = serial.Serial("/dev/" + name, rate)

        self.pose_calculator = PoseCalculator(PowerPortDetector(VideoLiveGenerator(port)))

    def convert_data(self):
        rot, trans = self.pose_calculator.get_values()

        #converts camera coordinates (trans) into robot coordinates <robotx, roboty, robotz>
        robotx = trans[0]
        roboty = math.cos(self.CAMERA_TILT)*trans[1]-math.sin(self.CAMERA_TILT)*trans[2]
        robotz = math.sin(self.CAMERA_TILT)*trans[1]+math.sin(self.CAMERA_TILT)*trans[2]

        #transformed camera coordinates (trans) to target coordinates
        targety = math.cos(rot[2])trans[1] - math.sin(rot[2])(-math.sin(rot[1])trans[2]+math.cos(rot[1])trans[2]))
        targetx = math.cos(rot[1])trans[0] + math.sin(rot[1])trans[2]
        targetz =  math.sin(rot[2])trans[1] + math.cos(rot[2])(-math.sin(rot[1])trans[2]+math.cos(rot[1])trans[2]))

        if trans[0] is None:
            return 9999, 9999, 9999

        return int(100 * robotx), int(100 * robotz), 10 * round(angle, 1)

    def send_data(self):
        x, y, z = self.convert_data()
        #self.s.write("S %04d %04d %.1s%04d E\n" % (x, y, "+" if z >= 0 else "-", abs(z)))
        self.s.write('S {:04d} {:04d} {:+04d} E\n'.format(x, y, z))

data_sender = DataSender()

while True:
    data_sender.send_data()
