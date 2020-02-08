import cv2


class VideoFileGenerator:
    def __init__(self, input_path):
        self.input_path = input_path
        self.input = cv2.VideoCapture(input_path)
        self.input.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.input.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        frame = self.get_frame()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

        self.H_FIELD_OF_VIEW = 68.37
        self.V_FIELD_OF_VIEW = 41.21

        self.capturing = True

    def __enter__(self):
        return self

    def get_frame(self):
        success, frame = self.input.read()
        if(success):
            return frame
        else:
            self.capturing = False
            return None

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW

    def generate(self):
        frame = self.get_frame()
        return frame, None

    def is_capturing(self):
        return self.capturing
