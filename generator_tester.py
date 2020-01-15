import argparse
import numpy as np
import time
from depth_data_generator import DepthDataGenerator
from depth_live_generator import DepthLiveGenerator


parser = argparse.ArgumentParser()
parser.add_argument("generator", help="which of the generator classes to test")
parser.add_argument("input_depth", help="path of the CSV file to read from")
parser.add_argument("input_image", help="path of the image file to read from")
parser.add_argument("destination", help="file to save the results to")
args = parser.parse_args()

if args.generator == "DepthDataGenerator":
    depth_data_generator = DepthDataGenerator(args.input_depth, args.input_image)
    arr, _ = depth_data_generator.generate()
    np.savetxt(args.destination, arr, delimiter=",", fmt="%s")
elif args.generator == "DepthLiveGenerator":
    depth_live_generator = DepthLiveGenerator(1)
    time.sleep(5)
    arr = depth_live_generator.generate()
    np.savetxt(args.destination, arr, delimiter=",", fmt="%s")
