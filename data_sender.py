import math
import numpy as np
import serial
from scipy.spatial.transform import Rotation as R
from pose_calculator import PoseCalculator
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:

    CAMERA_TILT = math.radians(30)  # update with the correct camera tilt angle

    def __init__(self, name="ttyS0", rate=9600, port=1):
        self.name = name
        self.rate = rate
        self.port = port

        self.s = serial.Serial("/dev/" + name, rate)

        self.pose_calculator = PoseCalculator(PowerPortDetector(VideoLiveGenerator(port)))

    def convert_data(self):
        rot, trans = self.pose_calculator.get_values()

        if trans[0] is None:
            return 9999, 9999, 9999

        dx = trans[2] * math.cos(math.radians(self.CAMERA_TILT))
        dy = trans[0]

        rot_x = np.array([[1, 0, 0],
                          [0, math.cos(math.radians(rot[0])), -math.sin(math.radians(rot[0]))],
                          [0, math.sin(math.radians(rot[0])), math.cos(math.radians(rot[0]))]])

        rot_y = np.array([[math.cos(math.radians(rot[1])), 0, math.sin(math.radians(rot[1]))],
                          [0, 1, 0],
                          [-math.sin(math.radians(rot[1])), 0, math.cos(math.radians(rot[1]))]])

        rot_z = np.array([[math.cos(math.radians(rot[2])), math.sin(math.radians(rot[2])), 0],
                          [-math.sin(math.radians(rot[2])), math.cos(math.radians(rot[2])), 0],
                          [0, 0, 1]])

        rot_c = np.array([[math.cos(self.CAMERA_TILT), 0, math.sin(self.CAMERA_TILT)],
                          [0, 1, 0],
                          [-math.sin(self.CAMERA_TILT), 0, math.cos(self.CAMERA_TILT)]])

        r_target = np.linalg.inv(rot_c) @ rot_z @ rot_y @ rot_x
        r = R.from_matrix(r_target)
        new_rotations = r.as_euler('zyx', degrees=True)
        angle = new_rotations[1]

        return int(100 * dx), int(100 * dy), 10 * round(angle, 1)

    def send_data(self):
        x, y, angle = self.convert_data()
        self.s.write(bytes('S {:04d} {:04d} {:+05d} E'.format(x, y, angle), "utf-8"))


data_sender = DataSender()

while True:
    data_sender.send_data()
