#!/bin/bash

# Source ros_packages
source projects/ros_packages/devel/setup.bash

# Arm UAV with mavros
rosrun mavros mavsys mode -c OFFBOARD
rosrun mavros mavsafety arm
