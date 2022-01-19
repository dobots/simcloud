#!/bin/bash 
roslaunch rosbridge_server rosbridge_websocket.launch port:=80 &
cd /webviz
npm run serve-static-webviz

