#!/bin/bash

# Setup PX4 Firmware variables
source /usr/px4/Tools/setup_gazebo.bash /usr/px4 /usr/px4/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/usr/px4/:/usr/px4/Tools/sitl_gazebo
