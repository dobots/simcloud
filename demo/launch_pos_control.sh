#!/bin/bash

# Source ros_packages
source projects/ros_packages/devel/setup.bash

# Start pos_control script
rosrun fire_station_pos_control FLYinCollapsedFireStation_rover.py