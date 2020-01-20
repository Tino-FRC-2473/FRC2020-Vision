import cv2


class VideoFileGenerator:
    def __init__(self, input_path):
        self.input_path = input_path
        self.input = cv2.VideoCapture(input_path)

        frame = self.get_frame()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

        self.H_FIELD_OF_VIEW = 70.42
        self.V_FIELD_OF_VIEW = 43.3

    def __enter__(self):
        return self

    def get_frame(self):
        success, frame = self.input.read()
        if(success):
            return frame
        return None

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW

    def generate(self):
        frame = self.get_frame()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None
