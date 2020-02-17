import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R

FOCAL_LENGTH = 657
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

camera_matrix = np.float64([[FOCAL_LENGTH, 0,            SCREEN_WIDTH / 2],
                            [0,            FOCAL_LENGTH, SCREEN_HEIGHT / 2],
                            [0,            0,            1]])

obj_points = np.array([[9.8125,  17, 0],
                       [-9.8125, 17, 0],
                       [-19.625,  0, 0],
                       [19.625,   0, 0]])

rx, ry, rz = 0, 0, 0
rvec = R.from_euler('xyz', [[rx, ry, rz]], degrees=True).as_rotvec()
tvec = np.float64([[0], [0], [72]])

img_points, _ = cv2.projectPoints(obj_points, rvec, tvec, camera_matrix, None)
img_points = img_points.reshape(4,2).astype(np.int64)
print(img_points)

frame = cv2.imread("black.png")
cv2.drawContours(frame, [img_points], -1, (0, 0, 255), 2)
cv2.imshow("frame", frame)
cv2.waitKey(1)
