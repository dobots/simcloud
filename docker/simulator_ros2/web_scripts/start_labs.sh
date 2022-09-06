#!/bin/bash

echo "Ip adress of host at $(hostname -i) "

source ./usr/local/nvm/nvm.sh

./usr/local/nvm/nvm.sh use stable

jupyter lab workspaces import /web_scripts/asimovo.jupyterlab-workspace

jupyter lab\
	--port=8888\
	--no-browser\
	--ip=0.0.0.0\
	--allow-root\
	--LabApp.token=''
