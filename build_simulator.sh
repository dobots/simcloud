#!/bin/bash

docker build . -t simulator -f docker/simulator/Dockerfile

echo
echo
echo "Start with:  docker/simulator/run.sh"

