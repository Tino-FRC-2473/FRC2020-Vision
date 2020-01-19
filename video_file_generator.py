import cv2
import math


class VideoFileGenerator:
    def __init__(self, input_path):
        self.input_path = input_path
        self.input = cv2.VideoCapture(input_path)

        frame = self.get_frame()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

        self.H_FIELD_OF_VIEW_RAD = 70.42 * math.pi / 180.0
        self.V_FIELD_OF_VIEW_RAD = 43.3 * math.pi / 180.0

    def __enter__(self):
        return self

    def get_frame(self):
        _, frame = self.input.read()
        return frame

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW_RAD

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW_RAD

    def generate(self):
        frame = self.get_frame()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None
