#!/bin/bash

cd /PX4/Firmware
source Tools/setup_gazebo.bash $PWD $PWD/build/px4_sitl_default

export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd):$(pwd)/Tools/sitl_gazebo
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/root/catkin_ws/src/mavlink/:/root/catkin_ws/src/mavros/
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/projects/ros_packages

cd /projects/ros_packages/


