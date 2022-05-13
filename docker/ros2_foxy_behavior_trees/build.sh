#!/bin/bash

docker build . -t ros2_foxy_behavior_trees -f ./Dockerfile

echo
echo
echo "Start with:  docker/ros2_foxy_behavior_trees/run.sh"

