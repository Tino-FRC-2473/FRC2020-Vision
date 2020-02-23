# CV spec
Specification for 2473's 2020 CV code

&nbsp;

## Vision input
Handles image, video, and camera input and generates arrays of RGB or depth data

### Responsibilities
- Finding camera parameters
- Field of view (FoV)
- Handle multiple cameras
- Synchronization

### Class structure
5 Generator classes
- `DepthDataGenerator` (single frame depth filename, still image filename)
- `DepthLiveGenerator` (RealSense camera port int)
- `ImageGenerator` (single image frame filename)
- `VideoFileGenerator` (filename)
- `VideoLiveGenerator` (camera port input int)

### API
####`get_horizontal_fov()`
Returns float degrees

####`get_vertical_fov()`
Returns float degrees

####`generate()`
Gets data for one frame.

Returns: `tuple(rgb ndarray shape (y, x, 3), depth ndarray shape(y,x))`.
For sources with no depth data, return `tuple(ndarray, None)`

&nbsp;

## Detection
Accurately detect any required target on the field

### Responsibilities
- Identify pixels that correspond to target (goal hexagon, balls)
- Construct contours around targets (goal hexagon)
- Color calibration to correct for lighting changes

### Class structure
1 class for each of 3 different targets. Constructor takes in a Generator
- `LoadingBayDetector` (not going to be used)
- `PowerPortDetector`
- `PowerCellDetector` for ball detection

### API
####`get_generator()`
Returns the contained Generator

####`run_detection()`
Calls \*`Generator.generate()`.

Returns tuple with:
- list of contours, one per target sorted by enclosed area
- mask showing detected target

`PowerCellDetector` returns a tuple with a list of balls (each with [x, y, radius]) and the generator's depth frame.

"Contour" is output of [cv2.findContours](https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours)
- For goal, return list with one contour (U shape)
- For loading, return list with two contours (inside and outside)
- For balls, return list with zero or more contours

&nbsp;

## Situational awareness
Utilizes contours from detection team to gain actionable data for the robot

### Responsibilities
- Position of camera relative to targets (3D position)
- Angle (3D)

### Class structure
1 `PoseCalculator` class. Constructor takes in a \*Detector object

### API
####`get_values()`
Calls \*`Detector.run_detection()`, intended for use with `PowerPortDetector` and `VideoLiveGenerator`

Returns: `tuple(Euler Rotation: [yaw, pitch, roll] in degrees, Position [x, y, z] in meters)`
- Ex. ([10º, 0º, 3º], [2m, 3m, 4m])
- These coordinates and rotations are defined in the camera coordinate system (the camera is at the origin).
- To go from object coordinate to camera coordinate, apply Rotation first, then translate by Position.
- if the target is not seen by camera, returns _`None`_ for all six values

####`get_balls()`
Calls \*`Detector.run_detection()`, intended for use with `PowerCellDetector` and `DepthLiveGenerator`

Returns `tuple(closest_balls, obstacle_present)`
- `closest_balls` is a list of the four closest balls.
  Each ball is represented by a list with [distance in m, angle in degrees].
  If there are less than four balls detected, the gaps are filled with an empty list [].
- `obstacle_present` is a boolean for whether or not an obstacle was detected.

&nbsp;

## Data sending
Sends data from PoseCalculator over serial for use by robot code.

### Responsibilities
- Using values from `PoseCalculator`'s `get_values()` and `get_balls()` and formatting them to what robot code needs
- Sending data over serial

### Class structure
- `DataSender`

### API
#### `send_data()`
Send distance from the robot to the target along the x and z axis, and the angle to the target over serial in the string format
`"S [+/-]x_distance [+-]z_distance [+/-]angle E\n"`

Examples:
- x = 296 cm, z = 1324 cm, angle = 123.4 degrees. Sends `"S +0296 +1324 +1234 E"`
- x = 907 cm, z = 89 cm, angle = -4.2 degrees. Sends `"S +0907 +0089 -0042 E"`

If robot does not detect target, sends `"S +9999 +9999 +9999 E"`

`send_data()` does not need to be used outside of data_sender.py; code is included in the file to run `send_data()` continuously.
Run `python3 data_sender.py` to use.

&nbsp;

## Jetson setup
Involves a collection of shell scripts to run on the Jetson.
run2020vision.sh is in the FRC2020-Vision repository and other setup/preparation scripts are in Jetson-Setup.

&nbsp;

## Driver/testing file
Common script for running any configuration of the CV pipeline. Stops running upon pressing the 'q' key or when the frame returned from the generator is None (for video files).

### Usage (WIP)
`run_cv.py [generator_type] [generator params...] [target_type]`

`python3 run_cv.py image -i test_photos_loading_bay/0degrees_18inches.png loading_bay`

A tester to play `Generator` output and capture depth frames is also available in `generator_tester.py`. Run `python3 generator_tester.py -h` or `python3 generator_tester.py --help` for options.