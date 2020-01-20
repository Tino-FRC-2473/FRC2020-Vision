import numpy as np
import csv
import cv2


class DepthDataGenerator:
    def __init__(self, depth_path, image_path):
        self.depth_file = open(depth_path, "r")
        self.image_path = image_path

        self.H_FIELD_OF_VIEW = 69.4
        self.V_FIELD_OF_VIEW = 42.5

    def __enter__(self):
        return self

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW

    def generate(self):
        depth_frame = []
        with self.depth_file as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                depth_frame.append(row)

        image = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)
        return np.asanyarray(image), np.asanyarray(depth_frame)
