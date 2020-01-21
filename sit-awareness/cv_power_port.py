import math
import cv2
import numpy as np
import subprocess
import imghdr
import traceback
import os
from math import sin, cos
from operator import add

# finds angle between robot's heading and the perpendicular to the targets
class VisionTargetDetector:

    # initilaze variables
    def __init__(self, input):

        self.input_path = input

        try:
            # if input is a camera port
            self.input = cv2.VideoCapture(int(input))
            # self.set_camera_settings(input)
        except:
            # if input is a path
            self.input = cv2.VideoCapture(input)

        self.input.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.input.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        frame = self.get_frame()

        self.previous_r = []
        self.previous_t = []

        # intialize screen width and screen height
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

        # intialize angle of field of view in radians
        self.FIELD_OF_VIEW_RAD = 70.42 * math.pi / 180.0

        # calculates focal length based on a right triangle representing the "image" side of a pinhole camera
        # ABC where A is FIELD_OF_VIEW_RAD/2, a is SCREEN_WIDTH/2, and b is the focal length
        self.FOCAL_LENGTH_PIXELS = (self.SCREEN_WIDTH / 2.0) / math.tan(self.FIELD_OF_VIEW_RAD / 2.0)

        # experimentally determined distance constant
        self.DISTANCE_CONSTANT = 1.359624061

        # number of previous values to keep for average
        self.NUM_VALS = 10

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.input.release()
        cv2.destroyAllWindows()
        print("exited")

    # sets exposure of the camera (will only work on Linux systems)
    def set_camera_settings(self, camera_port):

        camera_path = "/dev/video" + camera_port

        try:
            subprocess.check_call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_auto=1"])
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_absolute=1"])
        except:
            print("exposure adjustment not completed")

    # returns a frame corresponding to the input type
    def get_frame(self):

        frame = None

        # if input is a camera port, use VideoCapture()
        if self.input_path.isdigit():
            _, frame = self.input.read()
        # if input is an image, use cv2.imread()
        elif imghdr.what(self.input_path) is not None:
            frame = cv2.imread(self.input_path)
        # if input is a video, use VideoCapture()
        else:
            _, frame = self.input.read()

        return frame

    # convert rotation matrix to euler angles
    def get_euler_from_rodrigues(self, rmat):
        rx = 180*math.atan2(-rmat[2][1], rmat[2][2])/math.pi
        ry = 180*math.asin(rmat[2][0])/math.pi
        rz = 180*math.atan2(-rmat[1][0], rmat[0][0])/math.pi
        return rx, ry, rz

    # calculate rotation and translation vectors from contour trapezoid
    def get_angle_dist(self, trapezoid):

        obj_points = [[ 9.8125, 17, 0],
                      [-9.8125, 17, 0],
                      [-19.625,  0, 0],
					  [ 19.625,  0, 0]]

        img_points = []

        for p in trapezoid.get_points():
            img_points.append([p.x, p.y])

        frame = self.get_frame()

        obj_points = np.float64(obj_points)
        img_points = np.float64(img_points)

        #print("object", obj_points)
        #print("image", img_points)

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
            hull_changed.append([hull[i][0][0], hull[i][0][1]])

        max = 0
        max_arr = []
        for i in range(len(hull_changed)):
            for j in range(i):
                for k in range(j):
                    for m in range(k):
                        total = 0
                        total += math.hypot(hull_changed[i][0]-hull_changed[j][0],hull_changed[i][1]-hull_changed[j][1])
                        total += math.hypot(hull_changed[j][0]-hull_changed[k][0],hull_changed[j][1]-hull_changed[k][1])
                        total += math.hypot(hull_changed[k][0]-hull_changed[m][0],hull_changed[k][1]-hull_changed[m][1])
                        total += math.hypot(hull_changed[m][0]-hull_changed[i][0],hull_changed[m][1]-hull_changed[i][1])
                        if(total>max):
                            max = total
                            max_arr = [hull_changed[i],hull_changed[j],hull_changed[k],hull_changed[m]]

        arrmax_changed = []
        for i in range(len(max_arr)):
            arrmax_changed.append([max_arr[i]])
        return np.int0(arrmax_changed)

    def display_windows(self, frame, mask):
        cv2.imshow("contours: " + str(self.input_path), mask)
        cv2.imshow("frame: " + str(self.input_path), frame)

    def update_values(self, r, t):

        if len(self.previous_r) == self.NUM_VALS:
            self.previous_r.pop(0)

        if len(self.previous_t) == self.NUM_VALS:
            self.previous_t.pop(0)

        self.previous_r.append(r)
        self.previous_t.append(t)

    def get_avg_values(self):

        r_sum = [0, 0, 0]
        t_sum = [0, 0, 0]

        for i in range(3):
            r_sum[i] = sum(r[i] for r in self.previous_r)/len(self.previous_r)
            t_sum[i] = sum(t[i] for t in self.previous_t)/len(self.previous_t)

        return r_sum, t_sum

    def run_cv(self, display=True):

        frame = self.get_frame()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_green = np.array([65,145,65])
        high_green= np.array([87,255,229])

        # isolate the desired shades of green
        mask = cv2.inRange(hsv, low_green, high_green)

        # temporary fix until the Jetson is updated to opencv version 4
        if (cv2.__version__[0] == '3'):
            _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # sort contours by area in descending order
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

        if len(contours) < 1:
            self.display_windows(frame, mask)
            return [360, 360, 360], -1

        c = contours[0] # use the largest contour

        if cv2.contourArea(c) < 100:
            self.display_windows(frame, mask)
            return [360, 360, 360], -1

        corners = self.get_corners(c)
        area = cv2.contourArea(c)
        cv2.drawContours(frame, corners, -1, (0,0,255), 6)

        r, t = self.get_angle_dist(Trapezoid(corners, area))
        rmat, _ = cv2.Rodrigues(r) # convert rotation vector to matrix

        rx, ry, rz = self.get_euler_from_rodrigues(rmat)
        t *= self.DISTANCE_CONSTANT
        tx, ty, tz = t[0][0], t[1][0], t[2][0]

        self.update_values([rx, ry, rz], [tx, ty, tz])
        r, t = self.get_avg_values()

        # display values in the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "rx: " + str(round(r[0],2)), (20, self.SCREEN_HEIGHT - 90), font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "ry: " + str(round(r[1],2)), (20, self.SCREEN_HEIGHT - 60), font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "rz: " + str(round(r[2],2)), (20, self.SCREEN_HEIGHT - 30), font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "tx: " + str(round(t[0],2)), (int(self.SCREEN_WIDTH/2) + 20, self.SCREEN_HEIGHT - 90), font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "ty: " + str(round(t[1],2)), (int(self.SCREEN_WIDTH/2) + 20, self.SCREEN_HEIGHT - 60), font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "tz: " + str(round(t[2],2)), (int(self.SCREEN_WIDTH/2) + 20, self.SCREEN_HEIGHT - 30), font, 1, (255,255,255), 2, cv2.LINE_AA)

        # show windows
        if display:
            self.display_windows(frame, mask)

        return r, t

# this class defines a trapezoid
class Trapezoid:

    def __init__(self, box, area):
        self.box = box
        self.area = area
        self.points = []
        for coordinates in box:
            self.points.append(Point(coordinates[0][0], coordinates[0][1]))

    def get_center(self):
        x = sum(point.x for point in self.points) / 4
        y = sum(point.y for point in self.points) / 4
        return Point(x, y)

    def get_points(self):
        points = self.points
        mx, my = self.get_center().x, self.get_center().y

        def sort_clockwise(p):
            return (math.atan2(p.y - my, p.x - mx) + 2 * math.pi) % (2*math.pi)

        points.sort(key=sort_clockwise)
        return points

# this class defines a point
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinate(self):
        return [self.x, self.y]
