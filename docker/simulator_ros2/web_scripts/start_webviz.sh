#!/bin/bash 
source /opt/ros/noetic/setup.bash
roslaunch rosbridge_server rosbridge_websocket.launch port:=80 &
ros2 run ros1_bridge dynamic_bridge &
cd /webviz
npm run serve-static-webviz
