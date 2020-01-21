import os
import csv
import cv2
from cv_loading_bay import VisionTargetDetector

def remove_bracket(vectorVal):
	return float(str(vectorVal)[1:len(str(vectorVal)) - 1])

with open('vision_output.csv', mode='w', newline='') as output_file:
	output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	sorted_photos = sorted(os.listdir('test_photos_lb'))
	output_writer.writerow(["filename", "distance", "angle", "r1", "r2", "r3", "t1", "t2", "t3"])
	#for every filename
	for filename in sorted_photos:
		vtd = VisionTargetDetector('test_photos_lb/' + filename)
		print(filename)
		with vtd as v:
			r,t = v.run_cv()
			output_writer.writerow([filename, int(filename[filename.index('_')+1:-10]), int(filename[:filename.index('d')]),
								   remove_bracket(r[0]), remove_bracket(r[1]), remove_bracket(r[2]), remove_bracket(t[0]), remove_bracket(t[1]), remove_bracket(t[2])])


	#output_writer.close()
