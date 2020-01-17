import cv2


class ImageGenerator:
    def __init__(self, input_path):
        self.input_path = input_path

    def generate(self):
        frame = cv2.imread(self.input_path)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None
