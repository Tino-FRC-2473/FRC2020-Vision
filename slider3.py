import argparse
import math
import numpy as np
import cv2
from tkinter import *

class Visualization():

    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x400")
        self.create_elements()

    def create_elements(self):
        Label(self.root, text="rx").grid(row=0, column=0, padx=4, pady=4)

        self.rx = Scale(self.root, from_=-90, to=90, orient=HORIZONTAL, tickinterval=45, length=200)
        self.rx.grid(row=0, column=1, padx=4, pady=4)
        # self.ry = Scale(self, from_=-90, to=90, orient=HORIZONTAL, tickinterval=45, length=200)
        # self.ry.pack()
        # self.rz = Scale(self, from_=-90, to=90, orient=HORIZONTAL, tickinterval=45, length=200)
        # self.rz.pack()
        # self.button = Button(self, text='hi', command=self.quit)
        # self.button.pack()

    def set_values(self, rx, ry, rz):
        self.rx.set(rx)
        # self.ry.set(ry)
        # self.rz.set(rz)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("rx", help="degrees rotation around x axis")
    parser.add_argument("ry", help="degrees rotation around y axis")
    parser.add_argument("rz", help="degrees rotation around z axis")
    args = parser.parse_args()

    v = Visualization()
    v.set_values(args.rx, args.ry, args.rz)
    # v.master.title("hullo")
    v.mainloop()
