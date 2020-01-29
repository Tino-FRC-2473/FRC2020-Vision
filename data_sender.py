import serial
from pose_detector import PoseDetector
from loading_bay_detector import LoadingBayDetector
from power_port_detector import PowerPortDetector
from video_live_generator import VideoLiveGenerator


class DataSender:
    def __init__(self):
        name = "ttyTHS2"
        rate = 9600

        self.s = serial.Serial("/dev/" + name, rate)

        self.loading_bay_pd = PoseDetector(LoadingBayDetector(VideoLiveGenerator(1)))
        self.power_port_pd = PoseDetector(PowerPortDetector(VideoLiveGenerator(1)))

    def format_data(self):
        pass

    def send_data(self):
        self.s.write(data="")
