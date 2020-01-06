from tkinter import *
import argparse
import cv2

# parser = argparse.ArgumentParser()
# parser.add_argument("input", default="0 0 0")
# args = parser.parse_args(input)
# print(args)
#
slider = Tk()
slider.geometry("300x300")

def set_y_slider():
    y_input = y_entry.get()
    y.set(int(y_input))

def set_p_slider():
    p_input = p_entry.get()
    p.set(int(p_input))

def set_r_slider():
    r_input = r_entry.get()
    r.set(int(r_input))

y = Scale(slider, from_ = -180, to = 180, orient = HORIZONTAL)
y.pack()
y_entry = Entry(slider)
y_entry.pack();
y_but = Button(slider, text = "set yaw", width = 10, command=set_y_slider)
y_but.pack();

p = Scale(slider, from_ = -180, to = 180, orient = HORIZONTAL)
p.pack()
p_entry = Entry(slider)
p_entry.pack();
p_but = Button(slider, text = "set pitch", width = 10, command=set_p_slider)
p_but.pack();

r = Scale(slider, from_ = -180, to = 180, orient = HORIZONTAL)
r.pack()
r_entry = Entry(slider)
r_entry.pack()
r_but = Button(slider, text = "set roll", width = 10, command=set_r_slider)
r_but.pack();

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
