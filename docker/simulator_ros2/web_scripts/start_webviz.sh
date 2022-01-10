#!/bin/bash 
ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=80 &
cd /webviz
npm run serve-static-webviz
