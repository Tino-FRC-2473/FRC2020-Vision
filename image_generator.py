import cv2
import math


class ImageGenerator:
    def __init__(self, input_path):
        self.input_path = input_path

        self.H_FIELD_OF_VIEW = 68.37
        self.V_FIELD_OF_VIEW = 41.21
        self.CAMERA_TILT = math.radians(30)

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW

    def generate(self):
        frame = cv2.imread(self.input_path)
        return frame, None
