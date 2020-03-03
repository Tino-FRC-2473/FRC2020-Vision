#!/bin/bash

whoami

currdate=$(date)

cd /home/nvidia/FRC2020-Vision
sudo python3 data_sender.py > "cv_log_$(date +"%m-%d-%Y_%H-%M-%S").txt"
