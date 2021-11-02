#!/bin/bash

docker build . --no-cache -t ros_melodic_desktop_px4 -f docker/ros_melodic_desktop_px4/Dockerfile
echo
echo
echo 'Start with:  docker/ros_melodic_desktop_px4/run.sh'
