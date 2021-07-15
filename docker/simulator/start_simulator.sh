#!/bin/bash

#variables
export user_id="reka" sim_no="one"
web_terminal=true
gzweb=true

docker-compose -p _{$user_id}_{$sim_no} up -d

#start of the web terminal
if [ "$web_terminal" = true ] ; then
   docker exec -it -d $user_id"_"$sim_no"_simulator_1" ./web_scripts/start_web_terminal.sh
fi

#start of gzweb
if [ "$gzweb" = true ] ; then
   docker exec -it -d $user_id"_"$sim_no"_simulator_1" ./web_scripts/start_gzweb.sh
fi
