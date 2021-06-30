#!/bin/bash

export user_id="reka" sim_no="one"
docker-compose -p _{$user_id}_{$sim_no} up -d

#start of the web terminal
docker exec -it -d $user_id"_"$sim_no"_simulator_1" ./web_terminal_scripts/start_web_terminal.sh

#start of gzweb
#docker exec -it -d $user_id"_"$sim_no"_simulator_1" cd /gzweb && npm start
