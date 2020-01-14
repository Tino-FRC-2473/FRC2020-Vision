import numpy as np
import csv
import cv2


class DepthDataGenerator:
    def __init__(self, depthPath, imagePath):
        self.depthFile = open(depthPath, "r")
        self.imagePath = imagePath

    def __enter__(self):
        return self

    def generate(self):
        depthFrame = []
        with self.depthFile as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                depthFrame.append(row)

        image = cv2.cvtColor(cv2.imread(self.imagePath), cv2.COLOR_BGR2RGB)
        return np.asanyarray(depthFrame), image
