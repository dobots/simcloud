#!/bin/bash
. /rvizweb_ws/install/setup.bash
roslaunch rvizweb rvizweb.launch websocket_port:="80" config_file:=$1
