import cv2
import math
import subprocess


class VideoFileGenerator:
    
    def __init__(self, input_path):
        self.input_path = input_path
        self.input = cv2.VideoCapture(input_path)

        frame_number = 0
        frame = self.get_frame()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

    def __enter__(self):
        return self

    def set_camera_settings(self, camera_port):
        camera_path = "/dev/video" + camera_port

        try:
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_auto=1"])
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_absolute=1"])
        except FileNotFoundError:
            print("exposure adjustment not completed")

    def get_frame(self):
        _, frame = self.input.read()
        return frame

    def generate(self):
        frame = self.get_frame()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None
