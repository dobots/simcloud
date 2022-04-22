#!/bin/bash
#Auto generated launch file
set -m
shopt -u huponexit
source /source_me.bash
nohup ros2 launch gazebo_ros  gazebo.launch.py  gui:=false > /user_data/generated_launch_files/environments.log 2>&1 & disown
sleep 5
nohup ros2 launch rosbot_description rosbot_spawn.launch.py > /user_data/generated_launch_files/robot.log 2>&1 & disown
sleep 5
#Tools: console,gazebo,rviz 
cd /
nohup /web_scripts/start_gzweb.sh > /user_data/generated_launch_files/gzweb.log 2>&1 & disown
cd /
nohup /web_scripts/start_webviz.sh > /user_data/generated_launch_files/webviz.log 2>&1 & disown
 sleep 3
#curl --location --request GET https://appserver.flight2.dodedodo.com/configurator/simconfig_list/started/62471676416af400158930ac

