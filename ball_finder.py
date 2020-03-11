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
        self.floor_frame[self.floor_frame > 4] = 4

        # Displacement constants between rgb frame and depth frame
        self.DEPTH_X_SHIFT = -23
        self.DEPTH_Y_SHIFT = 31

        # Height of the camera (in m)
        self.CAMERA_HEIGHT = 0.7

        # Minimum distance (in m) for finding obstacles (the distance from the camera to the front of the robot)
        self.MIN_OBSTACLE_DIST = 0.56

    # Returns the center (x, y) of a contour based on its bounding box.
    def get_contour_center(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        return x + w / 2, y + h / 2

    # Returns horizontally straight distance (in m) to a ball or obstacle.
    # is_ball is used to determine whether or not to shift the x and y positions the amount needed when using the depth
    # camera.
    def get_distance_ball(self, depth_frame, ball):
        x = min(639, int(ball[0] + self.DEPTH_X_SHIFT))
        y = min(479, int(ball[1] + self.DEPTH_Y_SHIFT))

        depth_at_center = depth_frame[y, x]
        if self.CAMERA_HEIGHT < depth_at_center:
            return math.sqrt(math.pow(depth_at_center, 2) - math.pow(self.CAMERA_HEIGHT, 2))

        return depth_at_center

    def get_distance_obstacle(self, depth_frame, obstacle):
        mask = np.zeros((480, 640), dtype=np.uint8)
        cv2.drawContours(mask, [obstacle], 0, (255, 255, 255), thickness=cv2.FILLED)
        depth_mask = (mask == 255) * depth_frame
        cv2.imshow("Depth mask", depth_mask)
        return min(depth_mask[:, 1])

    # Returns angle (in degrees) between center of camera to center of ball.
    def get_angle_deg(self, ball):
        dist_to_center = ball[0] - self.SCREEN_WIDTH / 2
        return math.degrees(math.atan(dist_to_center / self.FOCAL_LENGTH_PIXELS))

    # Returns list of obstacle contours with area greater than 1000 pixels.
    def get_obstacles(self, depth, max_dist):
        if depth is None:
            return []

        without_floor = np.where(abs(depth - self.floor_frame) < 0.05, 0, depth)
        mask = cv2.inRange(without_floor, self.MIN_OBSTACLE_DIST, float(max_dist) - 0.05)
        obstacle_contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        obstacle_contours.sort(key=lambda obstacle: self.get_distance_obstacle(depth, obstacle))
        cv2.imshow("Obstacle contours", obstacle_contours)

        closest = next((obstacle for obstacle in obstacle_contours if cv2.contourArea(obstacle) > 1000), None)
        return None if closest is None else self.get_distance_obstacle(depth, closest)

    # Returns a tuple with:
    # - a list of the first four balls, each with [distance in m, angle in degrees]. If there are less than four balls,
    #   the gaps are filled with []
    # - a boolean representing whether or not an obstacle is present
    def get_balls(self):
        detected_balls, depth_frame = self.detector.run_detector()
        if not detected_balls or depth_frame is None:
            closest_obstacle_dist = self.get_obstacles(depth_frame, 3)
            return [[]] * 5, closest_obstacle_dist

        detected_balls.sort(key=lambda ball: self.get_distance_ball(depth_frame, ball, True))
        closest_balls = [[]] * 5
        for i in range(len(detected_balls[:5])):
            dist = self.get_distance_ball(depth_frame, detected_balls[i], True)
            angle = self.get_angle_deg(detected_balls[i])
            closest_balls[i] = [] if dist == 0 else [dist, angle]

        max_dist = next((ball[0] for ball in closest_balls if ball), 3)
        closest_obstacle_dist = self.get_obstacles(depth_frame, max_dist)

        return closest_balls, closest_obstacle_dist
