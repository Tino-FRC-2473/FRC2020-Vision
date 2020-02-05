import cv2
import numpy as np
import math
from loading_bay_detector import LoadingBayDetector
from video_live_generator import VideoLiveGenerator
from image_generator import ImageGenerator


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


# this class defines a point
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinate(self):
        return [self.x, self.y]

    def get_dist(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)
def sort_x(points):
	return points[0]
def sort_y(points):
	return points[1]


def dist(x1,y1,x2,y2):
	return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

img = cv2.imread("test_photos_loading_bay/0degrees_18inches.png")


detector = LoadingBayDetector(ImageGenerator("test_photos_loading_bay/0degrees_18inches.png"))
total_successes = 0;
for i in range(50):
    direction = "front"
    
    #_, img = vid.read()
    #img = img[:][::-1]
    
    
    contours = detector.run_detector()
    contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
    

    cv2.waitKey(1)
    successes = 0

    points = []
    for contour in contours:
        # epsilon = 0.2*cv2.arcLength(contour,True)
        # approx = cv2.approxPolyDP(contour,epsilon, True)
        approx = get_corners(contour)
        approx2 = []
        print(len(approx))
        for i in range(len(approx)):
        	approx2.append(approx[i])
        #print("hi")
        approx2.sort(key=sort_x)
        points.append(approx2)
        cv2.drawContours(img, [approx], -1, (0, 0, 255), 3)

    
    cv2.imshow("img", img)
    #cv2.imshow("mask", mask)

    if len(contours)<2:
        print("fail")
        continue
    margin_error = 0.15
    if len(points[0])<4 or len(points[1])<4:
        print("fail")
        continue


    print("testing left...")
    outer_left = dist(points[0][0][0],points[0][0][1],points[0][1][0],points[0][1][1])
    inner_left = dist(points[1][0][0],points[1][0][1],points[1][1][0],points[1][1][1])
    ratio_left = outer_left/inner_left

    if direction=="front":
        if abs(ratio_left-11/7)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="right":
        if abs(ratio_left-445/262)<margin_error:
           successes+=1
           print("success!")
        else:
           print("fail")
    elif direction=="left":
        if abs(ratio_left-344/234)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")

    print("left ratio: "+str(ratio_left)+"\n")

    print("testing right...")
    outer_right = dist(points[0][2][0],points[0][2][1],points[0][3][0],points[0][3][1])
    inner_right = dist(points[1][2][0],points[1][2][1],points[1][3][0],points[1][3][1])
    ratio_right = outer_right/inner_right

    if direction=="front":
        if abs(ratio_right-11/7)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="right":
        if abs(ratio_right-344/234)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="left":
        if abs(ratio_right-445/262)<margin_error:
           successes+=1
           print("success!")
        else:
           print("fail")
    print("right ratio: "+str(ratio_right)+"\n")

    for i in points:
    	i.sort(key=sort_y)

    print("testing top...")
    outer_top = dist(points[0][0][0],points[0][0][1],points[0][1][0],points[0][1][1])
    inner_top = dist(points[1][0][0],points[1][0][1],points[1][1][0],points[1][1][1])
    ratio_top = outer_top/inner_top
    if direction=="front":
        if abs(ratio_top-7/3)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="right":
        if abs(ratio_top-2.35)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="left":
        if abs(ratio_top-2.35)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    print("top ratio: "+str(ratio_top)+"\n")

    print("testing bottom...")
    outer_bottom = dist(points[0][2][0],points[0][2][1],points[0][3][0],points[0][3][1])
    inner_bottom = dist(points[1][2][0],points[1][2][1],points[1][3][0],points[1][3][1])
    ratio_bottom = outer_bottom/inner_bottom
    if direction=="front":
        if abs(ratio_bottom-7/3)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="right":
        if abs(ratio_bottom-2.35)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="left":
        if abs(ratio_bottom-2.35)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    print("bottom ratio: "+str(ratio_bottom)+"\n")
    

    print(str(successes)+" successes out of 4\n\n")
    if successes==4:
        total_successes+=1
print(total_successes)
    
     