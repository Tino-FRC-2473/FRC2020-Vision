# Vision Input Team:
Handles image, video, and camera input and generates arrays of RGB or depth data
## Responsibilities
- Finding Camera parameters
- Field of View (FoV)
- Handle multiple cameras
- Synchronization
## Class structure
4 ImageGenerator classes
- `DepthDataGenerator (single frame depth filename, still image filename)`
- `DepthLiveGenerator (Realsense camera port int)`
- `ImageGenerator (single image frame filename)`
- `VideoFileGenerator(filename)`
- `VideoLiveGenerator(camera port input int)`
## API
### get_horizontal_fov()
Returns float degrees

### get_vertical_fov()
Returns float degrees

### generate()
Gets data for one frame

Returns: `tuple(rgb ndarray shape (x, y, 3), depth ndarray shape(x,y))`
For sources with no depth data, return `tuple(ndarray, None)`

# Detection Team:
Accurately detect any required target on the field
## Responsibilities
- Identify pixels that correspond to target (goal hexagon, balls)
- Construct contours around targets (goal hexagon)
- Color calibration to correct for lighting changes
## Class structure
1 class for each of 3 different targets. Constructor takes in a ImageGenerator
- `LoadingBayDetector`
- `PowerPortDetector`
- `BallDetector`
## API
### get_generator()
Returns the contained ImageGenerator

### run_detection()
Calls ImageGenerator.generate()

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
Constructor takes in a *Detector object

## API
### run_cv()
Call Detector.run_detection()

Return: `tuple(Euler Rotation: (yaw, pitch, roll) in degrees, World Position (x, y, z) in meters)`
- Ex. ((10º, 0º, 3º), (2m, 3m, 4m))

# Driver/Testing file
Common script for running any configuration of the CV pipeline.  

## Usage (WIP)
`cv_runner.py --run_sitaware  [target_type] [generator_type] [generator params...]`

`python3 cv_runner.py VideoGenerator Ball`
