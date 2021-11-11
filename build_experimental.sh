#!/bin/bash

docker build . -t experimental -f docker/experimental/Dockerfile
echo
echo
echo 'Start with:  docker/experimental/run.sh'
