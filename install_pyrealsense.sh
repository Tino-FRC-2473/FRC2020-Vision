#!/bin/bash

sudo apt-get install git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev -y
sudo apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev -y

cd
sudo rm -rf librealsense/
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense/
yes "" | ./scripts/setup_udev_rules.sh
yes "" | ./scripts/patch-realsense-ubuntu-lts.sh

mkdir build
cd build
cmake ../ -DBUILD_PYTHON_BINDINGS=bool:true -DBUILD_EXAMPLES=true
sudo make -j4
sudo make install
export PYTHONPATH=$PYTHONPATH:/usr/local/lib
