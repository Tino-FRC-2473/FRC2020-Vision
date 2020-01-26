import cv2


class ImageGenerator:
    def __init__(self, input_path):
        self.input_path = input_path

        self.H_FIELD_OF_VIEW = 70.42
        self.V_FIELD_OF_VIEW = 43.3

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW

    def generate(self):
        frame = cv2.imread(self.input_path)
        return frame, None
        # return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), None
