#!/bin/bash

docker build . -t simulator_ros2_ignition -f ./Dockerfile

echo
echo
echo "Start with:  docker/simulator_ros2_ignition/run.sh"

