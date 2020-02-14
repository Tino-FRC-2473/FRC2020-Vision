import math
import numpy as np
import serial
from depth_live_generator import DepthLiveGenerator
from pose_calculator import PoseCalculator
from power_cell_detector import PowerCellDetector
from power_port_detector import PowerPortDetector
from scipy.spatial.transform import Rotation as R
from video_live_generator import VideoLiveGenerator


class DataSender:

    CAMERA_TILT = math.radians(30)  # update with the correct camera tilt angle

    def __init__(self, name="ttyS0", rate=9600, video_port=1, depth_port=2):
        self.s = serial.Serial("/dev/" + name, rate)
        self.pose_power_port = PoseCalculator(PowerPortDetector(VideoLiveGenerator(video_port)))
        self.pose_ball_detection = PoseCalculator(PowerCellDetector(DepthLiveGenerator(depth_port)))

    def get_power_port_data(self):
        rot, trans = self.pose_power_port.get_values()

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
        rotation = R.from_matrix(r_target)
        new_rotations = rotation.as_euler("zyx", degrees=True)
        angle = new_rotations[1]

        return int(100 * dx), int(100 * dy), int(10 * round(angle, 1))

    def get_ball_detection_data(self):
        ball_data = self.pose_ball_detection.get_balls()
        formatted = []

        for ball in ball_data:
            formatted.append([ball[0], ball[1]])  # add data formatting to this line

        return formatted

    def send_data(self):
        x, y, angle = self.get_power_port_data()
        data_to_send = "{:+05d} {:+05d} {:+05d}".format(x, y, angle)

        balls = self.get_ball_detection_data()
        for ball in balls:
            data_to_send += " "
            # add ball data to data_to_send here

        self.s.write(bytes("S " + data_to_send + " E", "utf-8"))


data_sender = DataSender()

while True:
    data_sender.send_data()
