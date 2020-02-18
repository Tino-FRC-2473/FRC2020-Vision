import os
import csv
import cv2
import argparse
from pose_calculator import PoseCalculator
from image_generator import ImageGenerator
from loading_bay_detector import LoadingBayDetector
from power_port_detector import PowerPortDetector

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory with test photos")
parser.add_argument("target", help="target to detect pose for", choices=["loading_bay", "power_port"])
parser.add_argument("--output", "-o", nargs="?", help="name of file to write to", default="output.csv")
parser.add_argument("--units", "-u", nargs="?", help="units to return distance in", choices=["in", "ft", "m"], default="m")
parser.add_argument("--display", "-d", action="store_true")
args = parser.parse_args()

with open(args.output, mode='w', newline='') as output_file:
    output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sorted_photos = sorted(os.listdir(args.dir))
    output_writer.writerow(["filename", "distance", "angle", "rx", "ry", "rz", "tx", "ty", "tz"])

    for filename in sorted_photos:
        generator = ImageGenerator(args.dir + "/" + filename)
        target_detector = None
        if args.target == "loading_bay":
            target_detector = LoadingBayDetector(generator)
        elif args.target == "power_port":
            target_detector = PowerPortDetector(generator)

        with PoseCalculator(target_detector) as pd:
            if args.display:
                while True:
                    r, t = pd.get_values(units=args.units, display=True)
                    key = cv2.waitKey(1)
                    if key == ord("n"):
                        break
                    elif key == ord("q"):
                        exit()
            else:
                r, t = pd.get_values(units=args.units, display=False)
                # example filename: 0degrees_18inches.png
                output_writer.writerow([filename, int(filename[filename.index('_')+1:filename.index(args.units[0])]), int(filename[:filename.index('d')]),
                                       r[0], r[1], r[2], t[0], t[1], t[2]])
