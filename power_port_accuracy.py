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


def dist(x1,y1,x2,y2):
	return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

detector = LoadingBayDetector(ImageGenerator("test_photos_power_port/0degrees_48inches.png"))
# starting_val = 0.01
#vid = cv2.VideoCapture(1)
total_successes = 0
for i in range(50):
    direction = "front"
    img = cv2.imread("test_photos_power_port/0degrees_48inches.png")

    #_, img = vid.read()
    #img = img[:][::-1]
    
    # img = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT) #blurs image
    contour = detector.run_detector()
    contour.sort(key=lambda c: cv2.contourArea(c), reverse=True)
    if len(contour)<1:
        print("failed")
        continue

    cv2.waitKey(1)
    successes = 0

    points = []
    
    epsilon = 0.01*cv2.arcLength(contour[0],True)
    # print("starting val:", starting_val)
    # starting_val = starting_val + 0.0001
    approx = cv2.approxPolyDP(contour[0], epsilon, True)
    cv2.drawContours(img, approx, -1, (0, 0, 255), 3)

    cv2.imshow("img", img)

    for i in range(len(approx)):
    	points.append(approx[i][0])
    #print("hi")
    points.sort(key=sort_x)

    
    margin_error = 0.08

    if len(points)<8:
        print("fail")
        continue

    outer_top_left = points[0]
    inner_top_left = points[1]
    outer_top_right = points[7]
    inner_top_right = points[6]

    points.sort(key=sort_y)

    outer_bottom_left = (0,0)
    inner_bottom_left = (0,0)
    outer_bottom_right = (0,0)
    inner_bottom_right = (0,0)

    if points[6][0]<points[7][0]:
        outer_bottom_left = points[6]
        outer_bottom_right = points[7]
    else:
        outer_bottom_left = points[7]
        outer_bottom_right = points[6]

    if points[5][0]<points[4][0]:
        inner_bottom_left = points[5]
        inner_bottom_right = points[4]
    else:
        inner_bottom_left = points[4]
        inner_bottom_right = points[5]



    print("testing left...")
    outer_left = dist(outer_top_left[0],outer_top_left[1],outer_bottom_left[0],outer_bottom_left[1])
    inner_left = dist(inner_top_left[0],inner_top_left[1],inner_bottom_left[0],inner_bottom_left[1])
    ratio_left = outer_left/inner_left

    if direction=="front":
        if abs(ratio_left-257.6/227.6)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="right":
        if abs(ratio_left-189.76/170.14)<margin_error:
           successes+=1
           print("success!")
        else:
           print("fail")
    elif direction=="left":
        if abs(ratio_left-313.93/267.2)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")

    print("left ratio: "+str(ratio_left)+"\n")

    print("testing right...")
    outer_right = dist(outer_top_right[0],outer_top_right[1],outer_bottom_right[0],outer_bottom_right[1])
    inner_right = dist(inner_top_right[0],inner_top_right[1],inner_bottom_right[0],inner_bottom_right[1])


    ratio_right = outer_right/inner_right

    if direction=="front":
        if abs(ratio_right-257.6/227.6)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="right":
        if abs(ratio_right-313.93/267.2)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="left":
        if abs(ratio_right-189.76/170.14)<margin_error:
           successes+=1
           print("success!")
        else:
           print("fail")
    print("right ratio: "+str(ratio_right)+"\n")

   
    print("testing bottom...")
    outer_bottom = dist(outer_bottom_left[0],outer_bottom_left[1],outer_bottom_right[0],outer_bottom_right[1])
    inner_bottom = dist(inner_bottom_left[0],inner_bottom_left[1],inner_bottom_right[0],inner_bottom_right[1])
    ratio_bottom = outer_bottom/inner_bottom
    if direction=="front":
        if abs(ratio_bottom-258/228)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="right":
        if abs(ratio_bottom-208.5/182.7)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    elif direction=="left":
        if abs(ratio_bottom-208.5/182.7)<margin_error:
            successes+=1
            print("success!")
        else:
            print("fail")
    print("bottom ratio: "+str(ratio_bottom)+"\n")

    

    print(str(successes)+" successes out of 3\n\n") 
    if successes==3:
        total_successes+=1
print(total_successes)