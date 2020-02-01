# Vision Input Team:
Handles image, video, and camera input and generates arrays of RGB or depth data

## Responsibilities
- Finding Camera parameters
- Field of View (FoV)
- Handle multiple cameras
- Synchronization

## Class structure
5 Generator classes
- `DepthDataGenerator` (single frame depth filename, still image filename)
- `DepthLiveGenerator` (RealSense camera port int)
- `ImageGenerator` (single image frame filename)
- `VideoFileGenerator` (filename)
- `VideoLiveGenerator` (camera port input int)

## API
### get_horizontal_fov()
Returns float degrees

### get_vertical_fov()
Returns float degrees

### generate()
Gets data for one frame

Returns: `tuple(rgb ndarray shape (y, x, 3), depth ndarray shape(y,x))`
For sources with no depth data, return `tuple(ndarray, None)`


# Detection Team:
Accurately detect any required target on the field

## Responsibilities
- Identify pixels that correspond to target (goal hexagon, balls)
- Construct contours around targets (goal hexagon)
- Color calibration to correct for lighting changes

## Class structure
1 class for each of 3 different targets. Constructor takes in a Generator
- `LoadingBayDetector`
- `PowerPortDetector`
- `BallDetector`

## API
### get_generator()
Returns the contained Generator

### run_detection()
Calls Generator.generate()

Returns: List of contours, one per target sorted by enclosed area

"Contour" is output of [cv2.findContours](https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours)
- For goal, return list with one contour (U shape)
- For loading, return list with two contours (inside and outside)
- For balls, return list with zero or more contours


# Situational Awareness:
Utilizes contours from detection team to gain actionable data for the robot

## Responsibilities
- Position of camera relative to targets (3D position)
- Angle (3D)

## Class Structure
1 PoseCalculator class
Constructor takes in a \*Detector object

## API
### get_values()
Call Detector.run_detection()

Return: `tuple(Euler Rotation: [yaw, pitch, roll] in degrees, Position [x, y, z] in inches)`
- Ex. ([10º, 0º, 3º], [2", 3", 4"])
- These coordinates and rotations are defined in the camera coordinate system (the camera is at the origin).
- To go from object coordinate to camera coordinate, apply Rotation first, then translate by Position.
- if the target is not seen by camera, returns _`None`_ for all six values


# Data Sending
Sends data from PoseCalculator over serial for use by robot code.

## Responsibilities
- Using values from PoseCalculator get_values() and formatting them to what robot code needs
- Sending data over serial

## Class structure
1 Data sender class
- `DataSender` ()

## API
### send_data()
Send distance from the robot to the target along the x and z axis, and the angle to the target over serial in the string format `"S x_distance z_distance [+/-]angle E\n"`


Examples:
- robotx = 296 cm, robotz = 1324 cm, angle = 123.4 degrees. Sends `"S 0296 1324 +1234 E\n"`
- robotx = 907 cm, robotz = 89 cm, angle = -4.2 degrees. Sends `"S 0907 0089 -0042 E\n"`

If robot does not detect target, sends `"S 9999 9999 +9999 E\n"`


# Driver/Testing file
Common script for running any configuration of the CV pipeline.  

## Usage (WIP)
`cv_runner.py --run_sitaware  [target_type] [generator_type] [generator params...]`

`python3 cv_runner.py VideoGenerator Ball`
