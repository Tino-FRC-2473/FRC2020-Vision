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

    def send_data(self):
        rot_l, trans_l = self.loading_bay_pd.get_values()
        rot_p, trans_p = self.power_port_pd.get_values()

        string = "S"

        for num in rot_l:
            string += format_data(num)

        for num in trans_l:
            string += format_data(num)

        for num in rot_p:
            string += format_data(num)

        for num in trans_p:
            string += format_data(num)

        self.s.write(string + "E")


def format_data(num):
    num = int(num)

    if num < -99:
        return "-99"
    if num > 999:
        return "999"
    if num < 0:
        return "-" + ("%02d" % -num)
    else:
        return "%03d" % num


data_sender = DataSender()

while True:
    data_sender.send_data()
