import math
import serial
from pose_calculator import PoseCalculator
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:

    CAMERA_TILT = 30  # update with the correct camera tilt angle

    def __init__(self):
        name = "ttyTHS2"
        rate = 9600  # update with the correct baudrate
        port = 1

        self.s = serial.Serial("/dev/" + name, rate)

        self.pose_calculator = PoseCalculator(PowerPortDetector(VideoLiveGenerator(port)))

    def convert_data(self):
        rot, trans = self.pose_calculator.get_values()

        robot_x = trans[0]
        robot_y = math.cos(self.CAMERA_TILT) * trans[1] - math.sin(self.CAMERA_TILT) * trans[2]
        robot_z = math.sin(self.CAMERA_TILT) * trans[1] + math.sin(self.CAMERA_TILT) * trans[2]

        target_x = trans[0] * math.cos(rot[1]) - trans[0] * math.sin(rot[1])
        target_y = trans[1] * math.cos(rot[0]) + trans[1] * math.sin(rot[0])
        target_z = (trans[2] *  (math.sin(rot[1]) + math.sin(rot[1]))) * (math.sin(rot[0]) + math.cos(rot[0]))

        angle = math.degrees(math.acos(target_y))

        if trans[0] is None:
            return 9999, 9999, 9999

        return int(100 * robot_x), int(100 * robot_z), 10 * round(angle, 1)

    def send_data(self):
        x, y, angle = self.convert_data()
        self.s.write('S {:04d} {:04d} {:+05d} E\n'.format(x, y, angle))


data_sender = DataSender()

while True:
    data_sender.send_data()
