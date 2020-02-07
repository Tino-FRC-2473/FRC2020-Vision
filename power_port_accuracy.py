import cv2
import numpy as np
import math

from image_generator import ImageGenerator
from power_port_detector import PowerPortDetector
from loading_bay_detector import LoadingBayDetector


def sort_x(points):
    return points[0]


def sort_y(points):
    return points[1]


# this class defines a point
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinate(self):
        return [self.x, self.y]

    def get_dist(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)


# simplify contour into four corner points
def get_corners(contour):

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


def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))


detector = LoadingBayDetector(ImageGenerator("test_photos_power_port/0degrees_60inches.png"))
# starting_val = 0.01
# vid = cv2.VideoCapture(1)
total_successes = 0
while True:
    direction = "front"
    img = cv2.imread("test_photos_power_port/0degrees_60inches.png")

    # _, img = vid.read()
    # img = img[:][::-1]

    # img = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT) #blurs image
    contour = detector.run_detector()
    contour.sort(key=lambda c: cv2.contourArea(c), reverse=True)
    if len(contour) < 1:
        print("failed")
        continue

    cv2.waitKey(1)
    successes = 0

    points = []
    approx = get_corners(contour[0])

    cv2.drawContours(img, [approx], -1, (0, 0, 255), 3)
    cv2.imshow("img", img)

    for i in range(len(approx)):
        points.append(approx[i])
    # print("hi")
    points.sort(key=sort_x)

    margin_error = 0.15

    if len(points) < 4:
        print("fail")
        continue

    top_left = points[0]
    top_right = points[3]

    points.sort(key=sort_y)

    bottom_left = (0, 0)

    bottom_right = (0, 0)

    if points[2][0] < points[3][0]:
        bottom_left = points[2]
        bottom_right = points[3]
    else:
        bottom_left = points[3]
        bottom_right = points[2]
    print("testing sides...")
    left = dist(top_left[0], top_left[1], bottom_left[0], bottom_left[1])
    right = dist(top_right[0], top_right[1], bottom_right[0], bottom_right[1])
    ratio_sides = left/right

    if direction == "front":
        if abs(ratio_sides-1) < margin_error:
            successes += 1
            print("success!")
        else:
            print("fail")
    elif direction == "right":
        if abs(ratio_sides-188.8/312.2) < margin_error:
            successes += 1
            print("success!")
        else:
            print("fail")
    elif direction == "left":
        if abs(ratio_sides-312.2/188.8) < margin_error:
            successes += 1
            print("success!")
        else:
            print("fail")

    print("side ratio: "+str(ratio_sides)+"\n")

    print("testing top and bottom...")
    top = dist(top_left[0], top_left[1], top_right[0], top_right[1])
    bottom = dist(bottom_left[0], bottom_left[1], bottom_right[0], bottom_right[1])
    ratio_tb = top/bottom
    if direction == "front":
        if abs(ratio_tb-258/228) < margin_error:
            successes += 1
            print("success!")
        else:
            print("fail")
    elif direction == "right":
        if abs(ratio_tb-425.15/207.63) < margin_error:
            successes += 1
            print("success!")
        else:
            print("fail")
    elif direction == "left":
        if abs(ratio_tb-425.15/207.63) < margin_error:
            successes += 1
            print("success!")
        else:
            print("fail")
    print("bottom ratio: "+str(ratio_tb)+"\n")

    print(str(successes)+" successes out of 2\n\n")
    if successes == 2:
        total_successes += 1
print(total_successes)
