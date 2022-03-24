#!/bin/bash

# Setup PX4 Firmware variables
source /PX4/Firmware/Tools/setup_gazebo.bash /PX4/Firmware /PX4/Firmware/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/PX4/Firmware:/PX4/Firmware/Tools/sitl_gazebo