import cv2
import argparse
from video_live_generator import VideoLiveGenerator

parser = argparse.ArgumentParser()
parser.add_argument("port", help="camera port to read from")
parser.add_argument("filename", help="file to write to")
args = parser.parse_args()

generator = VideoLiveGenerator(args.port)
frame, _ = generator.generate()
height, width = frame.shape[:2]
out = cv2.VideoWriter('output.avi', cv2.VideoWriter.fourcc(*'XVID'), 30, (width, height))

while (True):
    frame, _ = generator.generate()
    out.write(frame)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

out.release()
cv2.destroyAllWindows()
