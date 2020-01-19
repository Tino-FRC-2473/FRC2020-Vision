import cv2
import math


class ImageGenerator:
    def __init__(self, input_path):
        self.input_path = input_path

        self.H_FIELD_OF_VIEW_RAD = 70.42 * math.pi / 180.0
        self.V_FIELD_OF_VIEW_RAD = 43.3 * math.pi / 180.0

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW_RAD

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW_RAD

    def generate(self):
        frame = cv2.imread(self.input_path)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None
