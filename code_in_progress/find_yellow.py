import cv2
import os
import numpy as np
import math




def calc_ang(pinX):
    pin_dist_to_center = pinX - SCREEN_WIDTH / 2
    rad = math.atan(pin_dist_to_center/ FOCAL_LENGTH_PIXELS)
    deg = rad*180/math.pi
    return deg


directory = "test_photos"
true_yellow_vals = np.array([[5, 10, 15], [5, 10, 15]])
#print(true_yellow_vals.shape)
for filename in os.listdir(directory):
    #print(len(true_yellow_vals))
    if filename.endswith(".png"): 
        #print(os.path.join(directory, filename))


        img = cv2.imread(os.path.join(directory, filename))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for pixel in img[1,:,:]:
            true_yellow_vals = np.append(true_yellow_vals, [pixel], axis=0)
    


        continue
    else:
        continue

# print(true_yellow_vals.shape)
# print(true_yellow_vals[:,0])
# print(true_yellow_vals[:,1])
# print(true_yellow_vals[:,2])
max_x = max_y = 0
min_x = 1920
min_y = 1080

h = true_yellow_vals[:,0]
s = true_yellow_vals[:,1]
v = true_yellow_vals[:,2]


low_h, low_s, low_v = (h.mean() - 3.25 * h.std()), (s.mean() - 3.5 * s.std()), (v.mean() - 3.25 * v.std())
high_h, high_s, high_v = (h.mean() + 3.25 * h.std()), (s.mean() + 3.5 * s.std()), (v.mean() + 3.25 * v.std())

# print(low_h, low_s, low_v)
# print(high_h, high_s, high_v)

#vidcap = cv2.VideoCapture('test_photos/yellowcheck.mp4')
vidcap = cv2.VideoCapture(1)
FIELD_OF_VIEW_RAD = 67.823 * math.pi / 180.0
while True:
    low_yellow = np.array([17, 80, 80])
    high_yellow = np.array([40, 255, 255])

    # frame = cv2.imread("/Users/praneethguduguntla/Downloads/yellowcheck.mp4")

    _, frame = vidcap.read()
    frame = cv2.blur(frame,(5,5))
    SCREEN_HEIGHT, SCREEN_WIDTH = frame.shape[:2]
    FOCAL_LENGTH_PIXELS = (SCREEN_WIDTH / 2.0) / math.tan(FIELD_OF_VIEW_RAD / 2.0)
    
    hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# isolate the desired shades of green
    mask = cv2.inRange(hsv2, low_yellow, high_yellow)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    num = 0
    for contour in contours:


        (x,y,w,h) = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if(area < 700):
            continue
        if(w/h < 0.7 or w/h >1.8):
            continue

        if(y<SCREEN_HEIGHT/2):
            continue
        
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        if( not len(approx) > 8):
            continue

        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)
        print(num)
        num = num + 1

        cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
        cv2.putText(frame, str(calc_ang(x+w/2)), (int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)


    cv2.resize(frame, (960, 540))   
    cv2.resize(mask, (960, 540))   
    cv2.imshow("mask", mask)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
    

# vidcap = cv2.VideoCapture('/Users/praneethguduguntla/Desktop/yellowvals')
# success,image = vidcap.read()
# count = 0
# while success:
#   cv2.imwrite("/Users/praneethguduguntla/Downloads/YellowBallTraining/third_frame%d.jpg" % count, image)     # save frame as JPEG file      
#   success,image = vidcap.read()
#   print('Read a new frame: ', success)
#   count += 1