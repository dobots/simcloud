#!/bin/bash

source /PX4/Firmware/Tools/setup_gazebo.bash /PX4/Firmware /PX4/Firmware/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/PX4/Firmware:/PX4/Firmware/Tools/sitl_gazebo
# export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/root/catkin_ws/src/mavlink/:/root/catkin_ws/src/mavros/
# export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/projects/ros_packages/src