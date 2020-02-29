# Pre-match calibration plan

## Steps
1. Test floor subtraction
    - Show the colorized depth frame with a subtracted floor
    - Get human confirmation
    - If the floor frame is not good, allow testers to take a new floor photo and repeat the test until the floor frame works
2. Test power port green calibration
    - Show a frame with detected targets
    - Get human confirmation that calibration works with the current green values
    - If the green value starting bounds are not good, allow testers to pick a color from the current frame for low green and a color for high green
    - Repeat the test until calibration is good
3. Show accuracy results
    - Run accuracy tester
    - Output success percentage of target detection

## Structure
- `OnFieldCalibration` class
- `run_calibration()` method