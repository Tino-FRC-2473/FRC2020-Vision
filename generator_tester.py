import argparse
import numpy as np
import time
import cv2
from depth_data_generator import DepthDataGenerator
from image_generator import ImageGenerator
from video_live_generator import VideoLiveGenerator
from video_file_generator import VideoFileGenerator


parser = argparse.ArgumentParser()
parser.add_argument("generator", help="choices = [DepthDataGenerator, DepthLiveGenerator, ImageGenerator, VideoLiveGenerator, VideoFileGenerator]")
parser.add_argument("--destination", nargs="?", help="path of the file to save the results to")
parser.add_argument("--depth", nargs="?", help="path of the CSV file to read")
parser.add_argument("--image", nargs="?", help="path of the image file to read")
parser.add_argument("--video", nargs="?", help="path of the video file to read")
parser.add_argument("--play", action="store_true", help="specify whether or not to play live feeds or videos")
args = parser.parse_args()

if args.generator == "DepthDataGenerator":
    depth_data_generator = DepthDataGenerator(args.depth, args.image)
    rgb, depth = depth_data_generator.generate()
    np.savetxt(args.destination, depth, delimiter=",", fmt="%s")

elif args.generator == "DepthLiveGenerator":
    from depth_live_generator import DepthLiveGenerator
    depth_live_generator = DepthLiveGenerator(1)

    if not args.play:
        print("The tester will collect data after five seconds")
        time.sleep(5)
        rgb, depth = depth_live_generator.generate()
        if args.destination is not None:
            np.savetxt(args.destination, depth, delimiter=",", fmt="%s")
    else:
        print("Playing camera feed. Press \'q\' to quit")
        while True:
            bgr, depth = depth_live_generator.generate()
            cv2.imshow("Video", bgr)
            cv2.imshow("Depth", depth)
            key = cv2.waitKey(1)
            if key == ord('c') and args.destination is not None:
                np.savetxt(args.destination, depth, delimiter=",", fmt="%s")
            if key == ord('q'):
                break

elif args.generator == "ImageGenerator":
    image_generator = ImageGenerator(args.image)
    rgb, depth = image_generator.generate()
    print(rgb.shape)

elif args.generator == "VideoLiveGenerator":
    video_live_generator = VideoLiveGenerator(1)
    rgb, depth = video_live_generator.generate()
    print(rgb.shape)

    if args.play:
        print("Playing camera feed. Press \'q\' to quit")
        while True:
            rgb, _ = video_live_generator.generate()
            cv2.imshow("Live video", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

elif args.generator == "VideoFileGenerator":
    video_file_generator = VideoFileGenerator(args.video)
    rgb, depth = video_file_generator.generate()
    print(rgb.shape)

    if args.play:
        print("Playing camera feed. Press \'q\' to quit")
        while True:
            rgb, _ = video_file_generator.generate()
            cv2.imshow("Video", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
