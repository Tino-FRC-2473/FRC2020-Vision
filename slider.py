import argparse
import math
import numpy as np
import cv2
from tkinter import *
from scipy.spatial.transform import Rotation as R

FOCAL_LENGTH = 657
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# parser = argparse.ArgumentParser()
# parser.add_argument("rx", help="degrees rotation around x axis")
# parser.add_argument("ry", help="degrees rotation around y axis")
# parser.add_argument("rz", help="degrees rotation around z axis")
# args = parser.parse_args()

root = Tk()
root.geometry("320x490")
root.title("Transformation")

Label(root, text="rx").grid(row=0, column=0, padx=8, pady=4)
Label(root, text="ry").grid(row=1, column=0, padx=8, pady=4)
Label(root, text="rz").grid(row=2, column=0, padx=8, pady=4)
Label(root, text="tx").grid(row=3, column=0, padx=8, pady=4)
Label(root, text="ty").grid(row=4, column=0, padx=8, pady=4)
Label(root, text="tz").grid(row=5, column=0, padx=8, pady=4)
Label(root, text="focal length").grid(row=6, column=0, padx=8, pady=4)

rx_scale = Scale(root, from_=-90, to=90, orient=HORIZONTAL, tickinterval=45, length=200)
rx_scale.grid(row=0, column=1, padx=4, pady=4)
ry_scale = Scale(root, from_=-90, to=90, orient=HORIZONTAL, tickinterval=45, length=200)
ry_scale.grid(row=1, column=1, padx=4, pady=4)
rz_scale = Scale(root, from_=-90, to=90, orient=HORIZONTAL, tickinterval=45, length=200)
rz_scale.grid(row=2, column=1, padx=4, pady=4)

tx_scale = Scale(root, from_=-50, to=50, orient=HORIZONTAL, tickinterval=25, length=200)
tx_scale.grid(row=3, column=1, padx=4, pady=4)
ty_scale = Scale(root, from_=-50, to=50, orient=HORIZONTAL, tickinterval=25, length=200)
ty_scale.grid(row=4, column=1, padx=4, pady=4)
tz_scale = Scale(root, from_=0, to=320, orient=HORIZONTAL, tickinterval=80, length=200)
tz_scale.grid(row=5, column=1, padx=4, pady=4)

fl_scale = Scale(root, from_=300, to=1000, orient=HORIZONTAL, tickinterval=350, length=200)
fl_scale.grid(row=6, column=1, padx=4, pady=4)

tz_scale.set(72)
fl_scale.set(657)

# self.button = Button(self, text='hi', command=self.quit)
# self.button.pack()

def draw_points():

    FOCAL_LENGTH = fl_scale.get()

    camera_matrix = np.float64([[FOCAL_LENGTH, 0,            SCREEN_WIDTH / 2],
                                [0,            FOCAL_LENGTH, SCREEN_HEIGHT / 2],
                                [0,            0,            1]])

    obj_points = np.array([[9.8125,  17, 0],
                           [-9.8125, 17, 0],
                           [-19.625,  0, 0],
                           [19.625,   0, 0]])

    rx, ry, rz = rx_scale.get(), ry_scale.get(), rz_scale.get()
    tx, ty, tz = tx_scale.get(), ty_scale.get(), tz_scale.get()
    rvec = R.from_euler('xyz', [[rx, ry, rz]], degrees=True).as_rotvec()
    tvec = np.float64([[tx], [ty], [tz]])

    img_points, _ = cv2.projectPoints(obj_points, rvec, tvec, camera_matrix, None)
    img_points = img_points.reshape(4,2).astype(np.int64)

    frame = cv2.imread("black.png")
    cv2.drawContours(frame, [img_points], -1, (0, 0, 255), 2)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

    root.update()
    root.after(0, draw_points)

draw_points()
root.mainloop()
