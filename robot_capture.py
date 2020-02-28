import argparse
import os
import cv2
from video_live_generator import VideoLiveGenerator
from power_port_detector import PowerPortDetector

parser = argparse.ArgumentParser()
parser.add_argument("dir_name", help="directory to save images to")
parser.add_argument("port", help="camera port to read from")
parser.add_argument("filename", help="name of image")
args = parser.parse_args()

generator = VideoLiveGenerator(args.port)
target_detector = PowerPortDetector(generator)

if not os.path.isdir(args.dir_name):
    os.mkdir(args.dir_name)

filename = args.dir_name + "/" + args.filename
frame, _ = generator.generate()
cv2.imwrite(filename, frame)
