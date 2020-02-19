import math
import cv2
import numpy as np
import subprocess
import imghdr
import traceback
import os
from math import sin, cos
from operator import add
from scipy.spatial.transform import Rotation as R
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
        self.FOCAL_LENGTH_PIXELS = 657
        self.DISTANCE_CONSTANT = 0.9469335944
        self.NUM_VALS = 10  # number of previous values to keep for average

        self.FRAME_NAME = frame_name

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        cv2.destroyAllWindows()

    # calculate rotation and translation vectors
    def get_angle_dist(self, rectangle):

        img_points = []

        for p in rectangle.get_points():
            img_points.append([p.x, p.y])

        obj_points = np.float64(self.obj_points)
        img_points = np.float64(img_points)

        # img_points = np.array([[403, 406],
        #                        [247, 385],
        #                        [183, 240],
        #                        [499, 240]])

        camera_matrix = np.float64([[self.FOCAL_LENGTH_PIXELS, 0,                        self.SCREEN_WIDTH/2],
                                    [0,                        self.FOCAL_LENGTH_PIXELS, self.SCREEN_HEIGHT/2],
                                    [0,                        0,                        1]])

        # _, rvec, tvec, _ = cv2.solvePnPRansac(obj_points, img_points, camera_matrix, None, flags=cv2.SOLVEPNP_ITERATIVE, iterationsCount=100, reprojectionError=1.0, confidence=0.95)
        _, rvec, tvec = cv2.solvePnP(obj_points, img_points, camera_matrix, None)
        return rvec, tvec

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
            self.display_windows(frame, mask)
            return [None, None, None], [None, None, None]

        # sort contours by area in descending order
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
        c = contours[0]  # use the largest contour

        if cv2.contourArea(c) < 100:
            self.display_windows(frame, mask)
            return [None, None, None], [None, None, None]

        corners = self.get_corners(c)
        area = cv2.contourArea(c)
        cv2.drawContours(frame, [corners], -1, (0, 0, 255), 2)

        rvec, tvec = self.get_angle_dist(Target(corners, area))

        rot_c = np.array([[1, 0, 0],
                          [0, math.cos(self.generator.CAMERA_TILT), -math.sin(self.generator.CAMERA_TILT)],
                          [0, math.sin(self.generator.CAMERA_TILT), math.cos(self.generator.CAMERA_TILT)]])
        rmat = np.linalg.inv(rot_c) @ R.from_rotvec(rvec.flatten()).as_matrix()
        euler = R.from_matrix(rmat).as_euler('zyx', degrees=True)
        rx, ry, rz = euler[0], euler[1], euler[2]

        tvec = rot_c @ tvec.flatten()
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
