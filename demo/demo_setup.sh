#!/bin/bash

# Setup ros_packages
cd /projects/ros_packages/
catkin_make
source devel/setup.bash
# Setup px4
source /PX4/Firmware/Tools/setup_gazebo.bash /PX4/Firmware /PX4/Firmware/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/PX4/Firmware:/PX4/Firmware/Tools/sitl_gazebo

# Launch drone in fire_station simulation
roslaunch fire_station_description bringup_uav.launch

