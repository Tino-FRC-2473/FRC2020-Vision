import cv2


class ObstacleDetector:

    def __init__(self, generator):
        self.input = generator
       
    def run_detector(self):
        img, depth = self.input.generate()

        if img is None:
            return None, None

        low_distance = 0.5
        high_distance = 0.7

        mask = cv2.inRange(depth, low_distance, high_distance)
        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, mask

    def get_generator(self):
        return self.input

# 32 to 46 inches