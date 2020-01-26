import math
import cv2
import numpy as np
import subprocess
import imghdr
import traceback
import os
from math import sin, cos
from operator import add
# from depth_data_generator import DepthDataGenerator
# from depth_live_generator import DepthLiveGenerator
from image_generator import ImageGenerator
from video_file_generator import VideoFileGenerator
from video_live_generator import VideoLiveGenerator
from target_detector import TargetDetector


# finds rotation and translation of vision targets
class PoseDetector:

    # initilaze variables
    def __init__(self, detector, target):

        self.detector = detector
        self.generator = detector.get_generator()

        self.previous_r = []
        self.previous_t = []

        self.obj_points = []

        if target == "loading_bay":
            self.obj_points = [[3.5,   5.5, 0],
                               [-3.5,  5.5, 0],
                               [-3.5, -5.5, 0],
                               [3.5,  -5.5, 0]]
        elif target == "power_port":
            self.obj_points = [[9.8125,  17, 0],
                               [-9.8125, 17, 0],
                               [-19.625,  0, 0],
                               [19.625,   0, 0]]

        frame, _ = self.generator.generate()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]
        self.FOCAL_LENGTH_PIXELS = (self.SCREEN_WIDTH / 2.0) / math.tan(self.generator.get_horizontal_fov())

        # experimentally determined distance constant
        self.DISTANCE_CONSTANT = 1.359624061

        # number of previous values to keep for average
        self.NUM_VALS = 10

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        cv2.destroyAllWindows()
        print("exited")

    # convert rotation matrix to euler angles
    def get_euler_from_rodrigues(self, rmat):
        rx = 180 * math.atan2(-rmat[2][1], rmat[2][2]) / math.pi
        ry = 180 * math.asin(rmat[2][0]) / math.pi
        rz = 180 * math.atan2(-rmat[1][0], rmat[0][0]) / math.pi
        return rx, ry, rz

    # calculate rotation and translation vectors
    def get_angle_dist(self, rectangle):

        img_points = []

        for p in rectangle.get_points():
            img_points.append([p.x, p.y])

        obj_points = np.float64(self.obj_points)
        img_points = np.float64(img_points)

        camera_matrix = np.float64([[self.FOCAL_LENGTH_PIXELS, 0,                        self.SCREEN_WIDTH/2],
                                    [0,                        self.FOCAL_LENGTH_PIXELS, self.SCREEN_HEIGHT/2],
                                    [0,                        0,                        1]])

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
        cv2.imshow("frame", frame)

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
    def get_values(self, display=True):

        frame, _ = self.generator.generate()
        contours, mask = self.detector.run_detector()

        if len(contours) < 1:
            self.display_windows(frame, mask)
            return [360, 360, 360], -1

        # sort contours by area in descending order
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
        c = contours[0]  # use the largest contour

        if cv2.contourArea(c) < 100:
            self.display_windows(frame, mask)
            return [360, 360, 360], -1

        corners = self.get_corners(c)
        area = cv2.contourArea(c)
        cv2.drawContours(frame, [corners], -1, (0, 0, 255), 6)

        r, t = self.get_angle_dist(Target(corners, area))
        rmat, _ = cv2.Rodrigues(r)  # convert rotation vector to matrix

        rx, ry, rz = self.get_euler_from_rodrigues(rmat)
        t *= self.DISTANCE_CONSTANT
        tx, ty, tz = t[0][0], t[1][0], t[2][0]

        self.update_values([rx, ry, rz], [tx, ty, tz])
        r, t = self.get_avg_values()

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
        print(box)
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
