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
#### `get_horizontal_fov()`
Returns float degrees

#### `get_vertical_fov()`
Returns float degrees

#### `generate()`
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
#### `get_generator()`
Returns the contained Generator

#### `run_detection()`
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
Constructors take in a \*Detector object
- `PoseCalculator`
- `BallFinder`

### API
#### `PoseCalculator` `get_values()`
Calls \*`Detector.run_detection()`, intended for use with `PowerPortDetector` and `VideoLiveGenerator`

Returns: `tuple(Euler Rotation: [yaw, pitch, roll] in degrees, Position [x, y, z] in meters)`
- Ex. ([10º, 0º, 3º], [2m, 3m, 4m])
- These coordinates and rotations are defined in the camera coordinate system (the camera is at the origin).
- To go from object coordinate to camera coordinate, apply Rotation first, then translate by Position.
- if the target is not seen by camera, returns _`None`_ for all six values

#### `BallFinder` `get_balls()`
Calls \*`Detector.run_detection()`, intended for use with `PowerCellDetector` and `DepthLiveGenerator`

Returns `tuple(closest_balls, obstacle_present)`
- `closest_balls` is a list of the four closest balls.
  Each ball is represented by a list with [distance in m, angle in degrees].
  If there are less than four balls detected, the gaps are filled with an empty list [].
- `obstacle_present` is a boolean for whether or not an obstacle was detected.

&nbsp;

## Data sending
Sends data from `PoseCalculator` and `BallFinder` over serial for use by robot code.

### Responsibilities
- Using values from `PoseCalculator`'s `get_values()` and `BallFinder`'s `get_balls()` and formatting them to what robot code needs
- Sending data over serial

### Class structure
- `DataSender`

### API
#### `send_data()`
Sends data for the power port target, the closest five balls, and the closest obstacle in the way of the robot.

Data:
- Target:
    - target dy in cm
    - target dx in cm
    - target angle in degrees
- For each of five balls:
    - distance to ball in cm
    - angle to ball in degrees
- For obstacle:
    - distance to closest obstacle in cm

Each distance value is in the format "+9999", with a sign at the front and four digits following.

For all angles, the last digit is the tenths place after the decimal point. If the angle was -14.3 degrees, the value would be "-0143".

When no target is detected, the values for dy, dx, and angle are all "+9999". When less than five balls are detected, the distance and angle values for the rest of the spaces are also "+9999".

All values are surrounded by "S " at the start and " E" at the end, and values are separated by a single space in between.

Format:
```
"S +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 E"
    t_dy  t_dx  t_a   b1_d  b1_a  b2_d  b2_a  b3_d  b3_a  b4_d  b4_a  b5_d  b5_a  ob_d
    
('t' is the target, 'b1' is the first ball, and 'ob' is the obstacle. 'd' is distance and 'a' is the angle.)
```
In total, there are 14 values, all surrounded by "S " and " E".

Example for a situation where only one ball is seen:
```
dy       | dx       | angle        | ball1 dist       | ball1 angle      | obstacle     
----------------------------------------------------------------------------------------
296 cm   | 1324 cm  | 29.4 deg     | 152 cm           | -13.3 deg        | 98 cm

"S +0296 +1324 + 0294 +0152 -0133 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +9999 +0098 E"
```

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