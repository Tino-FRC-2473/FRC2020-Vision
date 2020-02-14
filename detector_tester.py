#!/usr/bin/env python3
import argparse
import pdb
import matplotlib.pyplot as plt

from image_generator import ImageGenerator
from power_port_detector import PowerPortDetector

parser = argparse.ArgumentParser()
parser.add_argument("image", help="path of the image file to read")
args = parser.parse_args()

generator = ImageGenerator(args.image)
target_detector = PowerPortDetector(generator)

contours, mask = target_detector.run_detector()

plt.figure()
plt.imshow(mask)
plt.title("Mask")
plt.show()
