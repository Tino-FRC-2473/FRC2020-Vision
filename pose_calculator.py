import math
import cv2
import numpy as np
import subprocess
import imghdr
import traceback
import os
from math import sin, cos
from operator import add
from loading_bay_detector import LoadingBayDetector
from power_port_detector import PowerPortDetector


# finds rotation and translation of vision targets
class PoseCalculator:

    # initilaze variables
    def __init__(self, detector, frame_name="frame"):
        self.detector = detector
        self.generator = detector.get_generator()

        self.previous_r = []
        self.previous_t = []

        self.obj_points = []

        # Depth csv of empty floor
        self.floor_frame = np.loadtxt("FLOOR.csv", dtype=np.float32, delimiter=',')

        if type(detector) is LoadingBayDetector:
            self.obj_points = [[3.5,   5.5, 0],
                               [-3.5,  5.5, 0],
                               [-3.5, -5.5, 0],
                               [3.5,  -5.5, 0]]
        elif type(detector) is PowerPortDetector:
            self.obj_points = [[9.8125,  17, 0],
                               [-9.8125, 17, 0],
                               [-19.625,  0, 0],
                               [19.625,   0, 0]]

        frame, _ = self.generator.generate()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]
        fov_radians = math.radians(self.generator.get_horizontal_fov())
        self.FOCAL_LENGTH_PIXELS = 657

        # experimentally determined distance constant
        self.DISTANCE_CONSTANT = 0.960144584
        # number of previous values to keep for average
        self.NUM_VALS = 10
        self.FRAME_NAME = frame_name

        self.CAMERA_TILT = math.radians(30)
        self.FRAME_NAME = frame_name

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        cv2.destroyAllWindows()

    # convert rotation matrix to euler angles
    def get_euler_from_rodrigues(self, rmat):
        rx = 180 * math.atan2(-rmat[2][1], rmat[2][2]) / math.pi
        ry = 180 * math.asin(rmat[2][0]) / math.pi
        rz = 180 * math.atan2(-rmat[1][0], rmat[0][0]) / math.pi
        return rx, ry, rz

    # calculate rotation and translation vectors
    def get_angle_dist(self, rectangle):

        img_points = []
        ret = True

        for p in rectangle.get_points():
            if (p.x <= 0 or p.y <= 0) or (p.x >= self.SCREEN_WIDTH - 1 or p.y >= self.SCREEN_HEIGHT - 1):
                ret = False
            img_points.append([p.x, p.y])

        obj_points = np.float64(self.obj_points)
        img_points = np.float64(img_points)

        camera_matrix = np.float64([[self.FOCAL_LENGTH_PIXELS, 0,                        self.SCREEN_WIDTH/2],
                                    [0,                        self.FOCAL_LENGTH_PIXELS, self.SCREEN_HEIGHT/2],
                                    [0,                        0,                        1]])

        # _, rvec, tvec, _ = cv2.solvePnPRansac(obj_points, img_points, camera_matrix, None, flags=cv2.SOLVEPNP_ITERATIVE, iterationsCount=100, reprojectionError=1.0, confidence=0.95)
        _, rvec, tvec = cv2.solvePnP(obj_points, img_points, camera_matrix, None)
        return rvec, tvec, ret

    # simplify contour into four corner points
    def get_corners(self, contour):

        hull = cv2.convexHull(contour)
        hull_changed = []
        for i in range(len(hull)):
            hull_changed.append(Point(hull[i][0][0], hull[i][0][1]))

        max = 0
        max_arr = []
        for i in range(len(hull_changed)):
            for j in range(i):
                for k in range(j):
                    for m in range(k):
                        total = hull_changed[i].get_dist(hull_changed[j])
                        total += hull_changed[j].get_dist(hull_changed[k])
                        total += hull_changed[k].get_dist(hull_changed[m])
                        total += hull_changed[m].get_dist(hull_changed[i])
                        if(total > max):
                            max = total
                            max_arr = [hull_changed[i], hull_changed[j], hull_changed[k], hull_changed[m]]

        arrmax_changed = []
        for i in max_arr:
            arrmax_changed.append([i.x, i.y])
        return np.int0(arrmax_changed)

    def display_windows(self, frame, mask):
        cv2.imshow("contours", mask)
        cv2.imshow(self.FRAME_NAME, frame)

    # update log of previous rotation and translation values
    def update_values(self, r, t):

        if len(self.previous_r) == self.NUM_VALS:
            self.previous_r.pop(0)

        if len(self.previous_t) == self.NUM_VALS:
            self.previous_t.pop(0)

        self.previous_r.append(r)
        self.previous_t.append(t)

    def get_contour_center(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        cx = x + w / 2
        cy = y + h / 2
        return cx, cy

    # Subtracts floor from current depth frame, returns new depth frame with removed floor values
    def subtract_floor(self, depth):
        floor = self.floor_frame.copy()
        floor[floor > 4] = 0
        subtracted = np.where(abs(depth - floor) < 0.05, 0, depth)
        return subtracted

    # Finds obstacles, returns list of obstacle contours with area greater than 1000 pixels
    def find_obstacles(self, depth, max_distance):
        if depth is None:
            return None

        removed_floor = self.subtract_floor(depth)
        cv2.imshow("subtracted", removed_floor)

        low_obstacle_distance = 0.56
        high_obstacle_distance = float(max_distance) - 0.05
        mask = cv2.inRange(removed_floor, low_obstacle_distance, high_obstacle_distance)
        cv2.imshow("Obstacles", mask)

        obstacle_contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        obstacle_contours.sort(key=lambda obstacle: self.get_distance_center(depth, self.get_contour_center(obstacle)[0], self.get_contour_center(obstacle)[1]))

        obstacles = []
        for obstacle in obstacle_contours:
            if cv2.contourArea(obstacle) > 1000:
                obstacles.append(obstacle)

        return obstacles

    # uses depth_frame to identify distance to (x, y)
    def get_distance_center(self, depth_frame, x, y):
        x = min(639, int(x))
        y = min(479, int(y))
        return depth_frame[y, x]

    # returns angle (in degrees) between center of camera to center of ball
    def calc_ang_deg(self, x):
        dist_to_center = x - self.SCREEN_WIDTH / 2
        return math.degrees(math.atan(dist_to_center / self.FOCAL_LENGTH_PIXELS))

    # returns distance and angle to the ball
    def get_balls(self):
        obstacle_present = False
        detected_balls, mask, color_frame, depth_frame = self.detector.run_detector()

        if detected_balls is None:
            obstacles = self.find_obstacles(depth_frame, 3)

            if obstacles is not None and len(obstacles) > 0:
                obstacle_present = True
                color_frame = cv2.drawContours(color_frame, obstacles, -1, (0, 255, 0), 3)

            cv2.imshow("color frame", color_frame)
            return None, obstacle_present

        # data[2] is the radius which we don't really need --> comes in the form [x, y, r]
        # sorts balls by distance (from RealSense depth data) in ascending order
        detected_balls.sort(key=lambda data: self.get_distance_center(depth_frame, data[0], data[1]))
        closest_balls = [None, None, None, None]

        for i in range(0, 4):
            if i < len(detected_balls):
                closest_balls[i] = detected_balls[i]

        # displacement constants between rgb frame and depth frame
        x_change = -23
        y_change = 31

        max_dist = self.get_distance_center(depth_frame, closest_balls[0][0] + x_change, closest_balls[0][1] + y_change)
        obstacles = self.find_obstacles(depth_frame, max_dist)

        if obstacles is not None and len(obstacles) > 0:
            obstacle_present = True
            color_frame = cv2.drawContours(color_frame, obstacles, -1, (0, 255, 0), 3)

        ball_data = []
        for ball in closest_balls:
            if ball is None:
                continue

            cv2.circle(color_frame, (int(ball[0]), int(ball[1])), int(ball[2]), (0, 0, 255), 3)
            cv2.circle(color_frame, (int(ball[0]), int(ball[1])), 0, (255, 0, 0), 6)

            dist = self.get_distance_center(depth_frame, ball[0] + x_change, ball[1] + y_change)
            if dist == 0:
                dist = self.get_distance_center(depth_frame, ball[0] + x_change + 10, ball[1] + y_change)

            angle = self.calc_ang_deg(ball[0])
            ball_data.append([dist, angle])

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(color_frame, "Distance: " + str(round(39.97 * dist, 2)),
                        (int(ball[0]), int(ball[1]) + int(ball[2])), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(color_frame, "Angle: " + str(round(angle, 2)),
                        (int(ball[0]), int(ball[1]) + int(ball[2]) + 20), font, 0.4, (255, 255, 255), 1,
                        cv2.LINE_AA)

        cv2.imshow("color frame", color_frame)

        return ball_data, obstacle_present

    # get average of previous rotation and translation values
    def get_avg_values(self):
        r_sum = np.mean(self.previous_r, axis=0)
        t_sum = np.mean(self.previous_t, axis=0)
        return r_sum.tolist(), t_sum.tolist()

    # runs pose detection code and returns rotation and translation
    def get_values(self, units="m", display=True):
        frame, _ = self.generator.generate()
        contours, mask = self.detector.run_detector()

        if contours is None:
            return [None, None, None], [None, None, None]

        if len(contours) < 1:
            if display:
                self.display_windows(frame, mask)
            return [None, None, None], [None, None, None]

        # sort contours by area in descending order
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
        c = contours[0]  # use the largest contour

        if cv2.contourArea(c) < 100:
            if display:
                self.display_windows(frame, mask)
            return [None, None, None], [None, None, None]

        corners = self.get_corners(c)
        area = cv2.contourArea(c)
        cv2.drawContours(frame, [corners], -1, (0, 0, 255), 2)

        rvec, tvec, ret = self.get_angle_dist(Target(corners, area))
        if not ret:
            if display:
                self.display_windows(frame, mask)
            return [None, None, None], [None, None, None]
        rmat, _ = cv2.Rodrigues(rvec)  # convert rotation vector to matrix

        rx, ry, rz = self.get_euler_from_rodrigues(rmat)
        ry -= 3.5
        rot = [rx, ry, rz]

        rot_x = np.array([[1, 0, 0], [0, math.cos(math.radians(rot[0])), -math.sin(math.radians(rot[0]))], [0, math.sin(math.radians(rot[0])), math.cos(math.radians(rot[0]))]])
        rot_y = np.array([[math.cos(math.radians(rot[1])), 0, math.sin(math.radians(rot[1]))], [0, 1, 0], [-math.sin(math.radians(rot[1])), 0, math.cos(math.radians(rot[1]))]])
        rot_z = np.array([[math.cos(math.radians(rot[2])), math.sin(math.radians(rot[2])), 0], [-math.sin(math.radians(rot[2])), math.cos(math.radians(rot[2])), 0], [0, 0, 1]])
        rot_camera = np.array([[1, 0, 0], [0, math.cos(self.generator.CAMERA_TILT), -math.sin(self.generator.CAMERA_TILT)], [0, math.sin(self.generator.CAMERA_TILT), math.cos(self.generator.CAMERA_TILT)]])

        r_target = np.linalg.inv(rot_camera) @ rot_z @ rot_y @ rot_x
        rx, ry, rz = self.get_euler_from_rodrigues(r_target)

        tvec = tvec.flatten()
        tvec = rot_camera @ tvec
        tvec *= self.DISTANCE_CONSTANT
        tx, ty, tz = tvec[0], tvec[1], tvec[2]

        self.update_values([rx, ry, rz], [tx, ty, tz])
        r, t = self.get_avg_values()

        if units == "m":
            t = [x / (12 * 3.281) for x in t]  # convert inches to meters
        elif units == "ft":
            t = [x / 12 for x in t]  # convert inches to feet

        # display values in the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "rx: " + str(round(r[0], 2)), (20, self.SCREEN_HEIGHT - 90), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "ry: " + str(round(r[1], 2)), (20, self.SCREEN_HEIGHT - 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "rz: " + str(round(r[2], 2)), (20, self.SCREEN_HEIGHT - 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "tx: " + str(round(t[0], 2)), (int(self.SCREEN_WIDTH/2) + 20, self.SCREEN_HEIGHT - 90), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "ty: " + str(round(t[1], 2)), (int(self.SCREEN_WIDTH/2) + 20, self.SCREEN_HEIGHT - 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "tz: " + str(round(t[2], 2)), (int(self.SCREEN_WIDTH/2) + 20, self.SCREEN_HEIGHT - 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # show windows
        if display:
            self.display_windows(frame, mask)

        return r, t


# this class defines a vision target
class Target:

    def __init__(self, box, area):
        self.box = box
        self.area = area
        self.points = []
        for coordinates in box:
            self.points.append(Point(coordinates[0], coordinates[1]))

    # return center of target as a Point object
    def get_center(self):
        x = sum(point.x for point in self.points) / 4
        y = sum(point.y for point in self.points) / 4
        return Point(x, y)

    # returns a sorted list of points
    def get_points(self):
        points = self.points
        center = self.get_center()

        # sort points clockwise, starting with the upper right point
        def sort_clockwise(p):
            return (math.atan2(p.y - center.y, p.x - center.x) + 2 * math.pi) % (2*math.pi)

        points.sort(key=sort_clockwise)
        return points


# this class defines a point
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinate(self):
        return [self.x, self.y]

    def get_dist(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)
