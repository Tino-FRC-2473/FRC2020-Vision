#!/usr/bin/env python3
import time
import argparse
import cv2
from pose_calculator import PoseCalculator
# from depth_data_generator import DepthDataGenerator
# from depth_live_generator import DepthLiveGenerator
from image_generator import ImageGenerator
from video_file_generator import VideoFileGenerator
from video_live_generator import VideoLiveGenerator
from loading_bay_detector import LoadingBayDetector
from power_port_detector import PowerPortDetector
from power_cell_detector import PowerCellDetector

# "python test.py 0" to run from camera in port 0
# "python test.py video.mp4" to run from the video recording video.mp4

parser = argparse.ArgumentParser()
parser.add_argument("generator", help="read from the given input type", choices=["depth_data", "depth_live", "image", "video_live", "video_file"])
parser.add_argument("--destination", "--dest", nargs="?", help="path of the file to save the results to")
parser.add_argument("--depth", "-d", nargs="?", help="path of the CSV file to read")
parser.add_argument("--image", "-i", nargs="?", help="path of the image file to read")
parser.add_argument("--video", "-v", nargs="?", help="path of the video file to read")
parser.add_argument("--port", "-p", nargs="?", help="camera port to read from")
parser.add_argument("--units", "-u", nargs="?", help="units to return distance in", choices=["in", "ft", "m"], default="m")
parser.add_argument("target", help="target to detect pose for", choices=["loading_bay", "power_port", "power_cell"])
args = parser.parse_args()

generator = None
wait_time = 1

if args.generator == "depth_data":
    generator = DepthDataGenerator(args.depth, args.image)
elif args.generator == "depth_live":
    generator = DepthLiveGenerator(args.port)
    wait_time = 3
elif args.generator == "image":
    generator = ImageGenerator(args.image)
elif args.generator == "video_live":
    generator = VideoLiveGenerator(args.port)
    wait_time = 3
elif args.generator == "video_file":
    generator = VideoFileGenerator(args.video)
    wait_time = int(1000./30) + 1

target_detector = None
if args.target == "loading_bay":
    target_detector = LoadingBayDetector(generator)
elif args.target == "power_port":
    target_detector = PowerPortDetector(generator)
elif args.target == "power_cell":
    target_detector = PowerCellDetector(generator)

with PoseCalculator(target_detector) as pc:
    while (generator.is_capturing() if args.generator == "video_file" else True):
        if type(target_detector) is PowerCellDetector:
            _, obstacle_present = pc.get_balls()
            print(obstacle_present)
        else:
            pc.get_values(units=args.units)

        key = cv2.waitKey(wait_time)
        if key == ord('q'):
            break
