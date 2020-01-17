import cv2
import numpy as np
from green_calibration import GreenCalibration
import math




def sort_x(points):
	return points[0]
def sort_y(points):
	return points[1]


def dist(x1,y1,x2,y2):
	return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

calibrator = GreenCalibration()

while True:
    img = cv2.imread("test_photos/0degrees_18inches.png")
    img = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT) #blurs image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, calibrator.LOW_GREEN, calibrator.HIGH_GREEN)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

    points = []
    for contour in contours:
        epsilon = 0.1*cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,epsilon, True)
        approx2 = []
        for i in range(len(approx)):
        	approx2.append(approx[i][0])
        #print("hi")
        approx2.sort(key=sort_x)
        points.append(approx2)
        cv2.drawContours(img, approx, -1, (0, 0, 255), 3)

    successes = 0
    print("testing left...")
    outer_left = dist(points[0][0][0],points[0][0][1],points[0][1][0],points[0][1][1])
    inner_left = dist(points[1][0][0],points[1][0][1],points[1][1][0],points[1][1][1])
    ratio_left = outer_left/inner_left
    if abs(ratio_left-11/7)<.5:
    	successes+=1
    	print("success!")
    else:
    	print("fail")
    print("left ratio: "+str(ratio_left)+"\n")

    print("testing right...")
    outer_right = dist(points[0][2][0],points[0][2][1],points[0][3][0],points[0][3][1])
    inner_right = dist(points[1][2][0],points[1][2][1],points[1][3][0],points[1][3][1])
    ratio_right = outer_right/inner_right
    if abs(ratio_right-11/7)<.5:
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
    if abs(ratio_top-7/3)<.5:
    	successes+=1
    	print("success!")
    else:
    	print("fail")
    print("top ratio: "+str(ratio_top)+"\n")

    print("testing bottom...")
    outer_bottom = dist(points[0][2][0],points[0][2][1],points[0][3][0],points[0][3][1])
    inner_bottom = dist(points[1][2][0],points[1][2][1],points[1][3][0],points[1][3][1])
    ratio_bottom = outer_bottom/inner_bottom
    if abs(ratio_bottom-7/3)<.5:
    	successes+=1
    	print("success!")
    else:
    	print("fail")
    print("bottom ratio: "+str(ratio_bottom)+"\n")
    

    print(str(successes)+" successes out of 4\n\n")

    greens = hsv[np.where((mask == 255))]
    calibrator.get_new_hsv(greens)
    cv2.imshow("img", img)
    cv2.imshow("mask", mask)

    cv2.waitKey(1)





