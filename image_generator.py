import cv2
import math


class ImageGenerator:
    def __init__(self, input_path):
        self.input_path = input_path

        self.FIELD_OF_VIEW = 70.42 * math.pi / 180.0

    def get_field_of_view(self):
        return self.FIELD_OF_VIEW

    def generate(self):
        frame = cv2.imread(self.input_path)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None
