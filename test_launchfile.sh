#!/bin/bash
#Auto generated launch file
set -m
shopt -u huponexit
source /source_me.bash
nohup roslaunch environments  collapsed_house.launch  gui:=false > ./environments.log 2>&1 & disown
sleep 5
nohup roslaunch uav spawn_uav.launch > ./robot.log 2>&1 & disown
sleep 5
#Tools: console,gazebo,rviz 
cd /
nohup /web_scripts/start_gzweb.sh > ./gzweb.log 2>&1 & disown
cd /
nohup /web_scripts/start_webviz.sh > ./webviz.log 2>&1 & disown
 sleep 3
# curl --location --request GET https://appserver.flight2.dodedodo.com/configurator/simconfig_list/started/6244104fecb556001bdfd139
