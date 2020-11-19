import numpy as np
import argparse
import os
import cv2
from image_generator import ImageGenerator

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory with photos")
args = parser.parse_args()

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

for image in os.listdir(args.dir):
    # print(image)
    generator = ImageGenerator(args.dir + "/" + image)
    img, _ = generator.generate()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        # Draw and display the cornerss
        cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
        # cv2.imshow('img', img)
        cv2.waitKey(200)
        ret, mtx, dist, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        print("matrix:", mtx)
        # print("dist:", dist)
        print("reprojection error:", ret)
        print("translation vector:", tvec)
        print("------------")

cv2.destroyAllWindows()
