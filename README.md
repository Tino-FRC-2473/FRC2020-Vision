# FRC2020-Vision
FRC 2473's CV code for 2020

# Project Organization
All Python code shall follow [PEP8 Style](https://www.python.org/dev/peps/pep-0008/)
- One file per Python class
- Import classes like `from depth_data_generator import DepthDataGenerator`

Each team will commit to one development branch. Team branches shall merge to master once a week. This implies that your code should be working and tested by the end of week cut-off time.
**Teams are responsible for ensuring that pull requests for their team branch are opened by Friday 9 PM. We will perform code reviews during Saturday meeting.**

# Environment Setup
For this year we will be using Python 3.8.1. Install Python from the [official website](https://www.python.org/downloads/release/python-381/). For Windows, make sure to check the option to add Python to your PATH and increase the PATH length limit.

Once the installer completes, open up a terminal (On Mac, use Terminal.app and on Windows, use CMD or Powershell). Run `python3 --version` to check the installation was succesful.

Next, install the Python packages we will be using with pip. 
`pip3 install --upgrade --user pip numpy scipy matplotlib networkx opencv-python serial`

Current dependency list:
* [Python 3.8.1](https://www.python.org/downloads/release/python-381/)
  * [numpy](https://docs.scipy.org/doc/numpy/reference/)
  * [scipy](https://docs.scipy.org/doc/scipy/reference/)
  * [matplotlib](https://matplotlib.org/api/index.html)
  * [OpenCV 4.1.2](https://docs.opencv.org/master/)
  * [networkx](https://networkx.github.io/documentation/stable/)
  * [serial](https://pyserial.readthedocs.io/en/latest/shortintro.html)
