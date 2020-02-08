import math
import serial
from pose_calculator import PoseCalculator
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:

    CAMERA_TILT = 30  # update with the correct camera tilt angle

    def __init__(self):
        name = "ttyS0"
        rate = 9600
        port = 1

        self.s = serial.Serial("/dev/" + name, rate)

        self.pose_calculator = PoseCalculator(PowerPortDetector(VideoLiveGenerator(port)))

    def convert_data(self):
        rot, trans = self.pose_calculator.get_values()

        if trans[0] is None:
            return 9999, 9999, 9999

        # robot_x = trans[0]
        # robot_y = math.cos(math.radians(self.CAMERA_TILT)) * trans[1] - math.sin(math.radians(self.CAMERA_TILT)) * trans[2]
        # robot_z = math.sin(math.radians(self.CAMERA_TILT)) * trans[1] + math.sin(math.radians(self.CAMERA_TILT)) * trans[2]
        # 
        # target_x = trans[0] * math.cos(math.radians(rot[1])) - trans[0] * math.sin(math.radians(rot[1]))
        # target_y = trans[1] * math.cos(math.radians(rot[0])) + trans[1] * math.sin(math.radians(rot[0]))
        # target_z = trans[2] * (math.sin(math.radians(rot[1])) + math.sin(math.radians(rot[1]))) * (math.sin(math.radians(rot[0])) + math.cos(math.radians(rot[0])))
        #
        # angle = math.degrees(math.acos(target_y))

        dx = trans[2] * math.cos(math.radians(self.CAMERA_TILT))
        dy = trans[0]
        angle = rot[1]

        return int(100 * dx), int(100 * dy), 10 * round(angle, 1)

    def send_data(self):
        x, y, angle = self.convert_data()
        self.s.write(bytes('S {:04d} {:04d} {:+05d} E'.format(x, y, angle), "utf-8"))


data_sender = DataSender()

while True:
    data_sender.send_data()
