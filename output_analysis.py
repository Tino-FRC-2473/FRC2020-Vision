import csv
import numpy as np
import argparse
from statistics import variance

parser = argparse.ArgumentParser()
parser.add_argument("input", help="CSV to read from")
parser.add_argument("--distance-constant", "-d", action="store_true")
args = parser.parse_args()

angle_errors = []
dist_errors = []
dist_constants = []

with open(args.input, newline='') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        angle, dist = float(row["angle"]), float(row["distance"])
        ry, tz = abs(float(row["ry"])), float(row["tz"])
        if angle == 0:
            angle_errors.append(abs(ry - angle))
        else:
            angle_errors.append(abs((ry - angle)) / angle)
        dist_errors.append(abs((tz - dist)) / dist)
        dist_constants.append(dist / tz)

print("average % angle error: ", round(100 * np.mean(angle_errors), 3))
print("average % distance error: ", round(100 * np.mean(dist_errors), 3))

if args.distance_constant:
    print("average distance constant: ", round(np.mean(dist_constants), 7))
    print("distance constant variance:", round(variance(dist_constants), 3))
