import cv2
import os
import numpy as np


directory = "/Users/praneethguduguntla/Desktop/yellowvals"
true_yellow_vals = np.array([[5, 10, 15], [5, 10, 15]])
print(true_yellow_vals.shape)
for filename in os.listdir(directory):
    print(len(true_yellow_vals))
    if filename.endswith(".png"): 
        print(os.path.join(directory, filename))


        img = cv2.imread(os.path.join(directory, filename))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for pixel in img[1,:,:]:
            true_yellow_vals = np.append(true_yellow_vals, [pixel], axis=0)
    


        continue
    else:
        continue

print(true_yellow_vals.shape)
print(true_yellow_vals[:,0])
print(true_yellow_vals[:,1])
print(true_yellow_vals[:,2])
max_x = max_y = 0
min_x = 1920
min_y = 1080

h = true_yellow_vals[:,0]
s = true_yellow_vals[:,1]
v = true_yellow_vals[:,2]


low_h, low_s, low_v = (h.mean() - 3.25 * h.std()), (s.mean() - 3.5 * s.std()), (v.mean() - 3.25 * v.std())
high_h, high_s, high_v = (h.mean() + 3.25 * h.std()), (s.mean() + 3.5 * s.std()), (v.mean() + 3.25 * v.std())

print(low_h, low_s, low_v)
print(high_h, high_s, high_v)

vidcap = cv2.VideoCapture('/Users/praneethguduguntla/Downloads/yellowcheck.mp4')
while True:
    low_yellow = np.array([17, 150, 150])
    high_yellow = np.array([33, 255, 255])

    # frame = cv2.imread("/Users/praneethguduguntla/Downloads/yellowcheck.mp4")

    _, frame = vidcap.read()
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
        
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        if( not len(approx) > 8):
            continue

        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)
        print(num)
        num = num + 1
        if w > 10 and h > 10:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)


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