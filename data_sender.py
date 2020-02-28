import argparse
import serial
from ball_finder import BallFinder
from depth_live_generator import DepthLiveGenerator
from pose_calculator import PoseCalculator
from power_cell_detector import PowerCellDetector
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:
    def __init__(self, name="ttyS0", rate=9600, video_port=1, depth_port=2, run_depth=True):
        self.s = serial.Serial("/dev/" + name, rate)
        self.pose_calculator = PoseCalculator(PowerPortDetector(VideoLiveGenerator(video_port)))
        self.ball_finder = BallFinder(PowerCellDetector(DepthLiveGenerator(depth_port)))
        self.run_depth = run_depth

    def get_power_port_data(self):
        rot, trans = self.pose_calculator.get_values()

        if trans[0] is None:
            return "+9999 +9999 +9999"

        dy = trans[0]
        dx = trans[2]
        angle = -rot[1]

        return "{:+05d} {:+05d} {:+05d}".format(int(100 * dx), int(100 * dy), int(10 * round(angle, 1)))

    def get_ball_detection_data(self):
        ball_data, obstacle_dist = self.ball_finder.get_balls()

        formatted = []
        for ball in ball_data:
            formatted.append([9999, 9999] if not ball else [int(100 * ball[0]), int(10 * round(ball[1], 1))])

        data_string = "".join(" {:+05d} {:+05d}".format(ball[0], ball[1]) for ball in formatted)
        data_string += " {:+05d}".format(int(100 * obstacle_dist)) if obstacle_dist else " +9999"

        return data_string

    def send_data(self):
        data_to_send = self.get_power_port_data()

        if self.run_depth:
            data_to_send += self.get_ball_detection_data()

        self.s.write(bytes("S " + data_to_send + " E", "utf-8"))


parser = argparse.ArgumentParser()
parser.add_argument("--video_port", "-v", type=int, default=1, help="camera port to read for VideoLiveGenerator")
parser.add_argument("--depth_port", "-d", type=int, default=2, help="camera port to read for DepthLiveGenerator")
parser.add_argument("--ignore_depth", "-i", action='store_false')
args = parser.parse_args()

data_sender = DataSender(video_port=args.video_port, depth_port=args.depth_port, run_depth=args.ignore_depth)

while True:
    data_sender.send_data()
