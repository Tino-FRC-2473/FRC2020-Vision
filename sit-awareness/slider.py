from tkinter import *
import argparse
import math
import numpy as np
import cv2

# parser = argparse.ArgumentParser()
# parser.add_argument("input", default="0 0 0")
# args = parser.parse_args(input)
# print(args)
parser = argparse.ArgumentParser()
parser.add_argument("input", help="read from the given camera or file", default="0")
args = parser.parse_args()

slider = Tk()
slider.geometry("300x300")

def set_y_slider():
    y_input = y_entry.get()
    # if y_input is None:
    #     y_input = y.get()
    y.set(float(y_input))

def set_p_slider():
    p_input = p_entry.get()
    # if p_input is None:
    #     p_input = p.get()
    p.set(float(p_input))

def set_r_slider():
    r_input = r_entry.get()
    # if r_input is None:
    #     r_input = r.get()
    r.set(float(r_input))

def test_values():
    yaw = math.pi * y.get() / 180.0
    pitch = math.pi * p.get() / 180.0
    roll = math.pi * r.get() / 180.0

    # print("hello:", yaw, pitch, roll)

    yaw_mat = np.matrix([[math.cos(yaw), -math.sin(yaw), 0],
                        [math.sin(yaw), math.cos(yaw), 0],
                        [0, 0, 1]
                        ]) #z
    pitch_mat = np.matrix([[math.cos(pitch), 0, math.sin(pitch)],
                            [0, 1, 0],
                            [-math.sin(pitch), 0, math.cos(pitch)]
                            ]) #y
    roll_mat = np.matrix([[1, 0, 0],
                          [0, math.cos(roll), -math.sin(roll)],
                          [0, math.sin(roll), math.cos(roll)]
                          ]) #x

    rot = yaw_mat * pitch_mat * roll_mat
    # print(rot[2, 0])
    # print(rot[2][0])
    translated = cv2.Rodrigues(rot)[0]

    # print("type:", type(cv2.Rodrigues(rot)))
    # print(cv2.Rodrigues(rot))

    print(rot)
    print(translated)
    # theta = math.acos(((rot[0, 0] + rot[1, 1] + rot[2, 2]) - 1) / 2)
    # multi = 1 / (2 * math.sin(theta))
    # print([yaw, pitch, roll])
    # use project points function in opencv
    obj_points = [[ 0.0,  0.0, 0],
                  [ 3.5,  5.5, 0],
                  [-3.5,  5.5, 0],
                  [-3.5, -5.5, 0],
                  [ 3.5, -5.5, 0],
                  [ 1.5,  3.5, 0],
                  [-1.5,  3.5, 0],
                  [-1.5, -3.5, 0],
                  [ 1.5, -3.5, 0]]
    # mx = rectangles[0].get_center().x
    # my = rectangles[0].get_center().y
    #
    # img_points = []
    # img_points.append([0,0])
    #
    # for r in rectangles:
    #     for p in r.get_points():
    #         img_points.append([p.x - mx, p.y - my])

    obj_points = np.float64(obj_points)
    test_tvec = (0, 0, 0)

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480


    # intialize angle of field of view in radians
    FIELD_OF_VIEW_RAD = 70.42 * math.pi / 180.0

    # calculates focal length based on a right triangle representing the "image" side of a pinhole camera
    # ABC where A is FIELD_OF_VIEW_RAD/2, a is SCREEN_WIDTH/2, and b is the focal length
    FOCAL_LENGTH_PIXELS = (SCREEN_WIDTH / 2.0) / math.tan(FIELD_OF_VIEW_RAD / 2.0)
    distance_co = []
    camera_matrix = np.float64([[FOCAL_LENGTH_PIXELS, 0,                        SCREEN_WIDTH/2],
                                [0,                        FOCAL_LENGTH_PIXELS, SCREEN_HEIGHT/2],
                                [0,                        0,                        1]])

    img_points = np.array(cv2.projectPoints(obj_points, translated, test_tvec, camera_matrix, None))[0]
    print(img_points)


    # frame = cv2.imread(args.input)
    # cv2.drawContours(frame, img_points, -1, (0,255,0), 6)



y = Scale(slider, from_ = -180, to = 180, orient = HORIZONTAL)
y.pack()
y_entry = Entry(slider)
y_entry.pack()
y_but = Button(slider, text = "set yaw", width = 10, command=set_y_slider)
y_but.pack()

p = Scale(slider, from_ = -180, to = 180, orient = HORIZONTAL)
p.pack()
p_entry = Entry(slider)
p_entry.pack()
p_but = Button(slider, text = "set pitch", width = 10, command=set_p_slider)
p_but.pack()

r = Scale(slider, from_ = -180, to = 180, orient = HORIZONTAL)
r.pack()
r_entry = Entry(slider)
r_entry.pack()
r_but = Button(slider, text = "set roll", width = 10, command=set_r_slider)
r_but.pack()

test_but = Button(slider, text = "test values", width = 10, command=test_values)
test_but.pack()

mainloop()

# while (True):
#     y_input = y_entry.get()
#     y.set(int(y_input))
#     # p_input = p_entry.get()
#     # p.set(int(p_entry))
#     # r_input = r_entry.get()
#     # r.set(int(r_entry))
#     key = cv2.waitKey(3)
#     if key == word('q'):
#         break
# # y.set(sliderVal.integer)
# def sel():
#    selection = "Value = " + str(var.get())
#    label.config(text = selection)
#
# root = Tk()
# var = DoubleVar()
# scale = Scale( root, variable = var )
# scale.pack(anchor=CENTER)
#
# button = Button(root, text="Get Scale Value", command=sel)
# button.pack(anchor=CENTER)
#
# label = Label(root)
# label.pack()
# root.mainloop()
