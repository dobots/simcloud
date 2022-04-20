#!/bin/bash

docker build . -t simulator_ros2 -f ./Dockerfile

echo
echo
echo "Start with:  docker/simulator_ros2/run.sh"

