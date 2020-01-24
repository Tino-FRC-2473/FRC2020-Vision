import subprocess
import time
import cv2


camera_port = 1

try:
    subprocess.call(["v4l2-ctl", "-d", "/dev/video" + str(camera_port), "-c", "exposure_auto=1"])
    subprocess.call(["v4l2-ctl", "-d", "/dev/video" + str(camera_port), "-c", "exposure_absolute=1"])
except FileNotFoundError:
    print("Exposure adjustment failed")

cap = cv2.VideoCapture(camera_port)

if cap.isOpened() is False:
    print("Unable to read camera feed")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

counter = 0

while True:
    start_time = time.time()

    out = cv2.VideoWriter('output' + str(counter) + '.avi',
                          cv2.VideoWriter_fourcc(*'XVID'), 10, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()

        if ret:
            out.write(frame)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()
        else:
            break

        if time.time() - start_time >= 15:
            break

    out.release()

    print("Wrote output" + str(counter) + ".avi")
    counter = counter + 1

    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()
