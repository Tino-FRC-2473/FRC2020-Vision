import numpy as np
import cv2 as cv


#vidcap = cv.VideoCapture('test_photos_balls/yellowcheck.mp4')
#vidcap = cv.VideoCapture(1)
#vidcap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
#vidcap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    low_yellow = np.array([17, 120, 120])
    high_yellow = np.array([33, 255, 255])

    img = cv.imread('./test_photos_balls/realfield3.png')

    #_, img = vidcap.read()
    HEIGHT = img.shape[0]

    output = img.copy()
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv = cv.medianBlur(hsv, 5)


    mask = cv.inRange(hsv, low_yellow, high_yellow)
    mask = cv.erode(mask,None, iterations=7)
    mask = cv.dilate(mask,None, iterations=10)

    print(mask.dtype)
    print(hsv[:,:,1].dtype)
    print(hsv[:,:,1].shape)
    print(mask.shape)
    print(type(mask))

    output = cv.bitwise_and(hsv, hsv, mask = mask)
    cv.imshow("hsv", output[:,:,2])

    th2 = cv.adaptiveThreshold(output[:,:,2], 255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,15,10)

    circles = cv.HoughCircles(th2, cv.HOUGH_GRADIENT, 1.8, 40, param1=70, param2=50, minRadius=20, maxRadius=60)

    if(circles is None):
        print("found no circles")
        cv.imshow('output',output)
        continue

    
    cv.imshow("hsv", mask)

    detected_circles = np.uint16(np.around(circles))
    for (x, y ,r) in detected_circles[0, :]:
        if(y < HEIGHT/2):
            continue

        
        cv.circle(img, (x, y), r, (0, 0, 255), 3)
        cv.circle(img, (x, y), 2, (255, 0, 0), 1)


    cv.imshow('output',img)
    cv.waitKey(1)
cv.destroyAllWindows()

