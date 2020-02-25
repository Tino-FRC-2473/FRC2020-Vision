import cv2
import math
import numpy as np


class BallFinder:
    def __init__(self, detector):
        self.detector = detector
        self.generator = detector.get_generator()

        frame, _ = self.generator.generate()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]
        self.FOCAL_LENGTH_PIXELS = 657

        # Depth csv of empty floor
        self.floor_frame = np.loadtxt("FLOOR.csv", dtype=np.float32, delimiter=",")
        self.floor_frame[self.floor_frame > 4] = 0

        # Displacement constants between rgb frame and depth frame
        self.DEPTH_X_SHIFT = -23
        self.DEPTH_Y_SHIFT = 31

        # Minimum distance (in m) for finding obstacles (the distance from the camera to the front of the robot)
        self.MIN_OBSTACLE_DIST = 0.56

    # Returns depth frame where all floor points have depth 0.
    def remove_floor(self, depth):
        return np.where(abs(depth - self.floor_frame) < 0.05, 0, depth)

    # Returns the center (x, y) of a contour based on its bounding box.
    def get_contour_center(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        return x + w / 2, y + h / 2

    # Returns distance (in m) to a ball or obstacle.
    # is_ball is used to determine whether or not to shift the x and y positions the amount needed when using the depth
    # camera.
    def get_distance(self, depth_frame, item, is_ball=False):
        x = min(639, int(item[0] + is_ball * self.DEPTH_X_SHIFT))
        y = min(479, int(item[1] + is_ball * self.DEPTH_Y_SHIFT))
        return depth_frame[y, x]

    # Returns angle (in degrees) between center of camera to center of ball.
    def get_angle_deg(self, ball):
        dist_to_center = ball[0] - self.SCREEN_WIDTH / 2
        return math.degrees(math.atan(dist_to_center / self.FOCAL_LENGTH_PIXELS))

    # Returns list of obstacle contours with area greater than 1000 pixels.
    def get_obstacles(self, depth, max_distance):
        if depth is None or not max_distance:
            return []

        mask = cv2.inRange(self.remove_floor(depth), self.MIN_OBSTACLE_DIST, float(max_distance) - 0.05)
        obstacle_contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        obstacle_contours.sort(key=lambda obstacle: self.get_distance(depth, self.get_contour_center(obstacle)))
        obstacles = list(filter(lambda obstacle: cv2.contourArea(obstacle) > 1000, obstacle_contours))
        cv2.imshow("Obstacles", mask)
        return obstacles

    # Returns a tuple with:
    # - a list of the first four balls, each with [distance in m, angle in degrees]. If there are less than four balls,
    #   the gaps are filled with []
    # - a boolean representing whether or not an obstacle is present
    def get_balls(self):
        detected_balls, depth_frame = self.detector.run_detector()
        if not detected_balls or depth_frame is None:
            obstacles = self.get_obstacles(depth_frame, 3)
            return [[]] * 4, len(obstacles) > 0

        detected_balls.sort(key=lambda ball: self.get_distance(depth_frame, ball, True))
        closest_balls = [[]] * 4
        for i in range(len(detected_balls[:4])):
            dist = self.get_distance(depth_frame, detected_balls[i], True)
            angle = self.get_angle_deg(detected_balls[i])
            closest_balls[i] = [] if dist == 0 else [dist, angle]

        max_dist = 3 if not closest_balls[0] else closest_balls[0][0]
        obstacles = self.get_obstacles(depth_frame, max_dist)

        for ball in closest_balls:
            print(ball)

        return closest_balls, len(obstacles) > 0
