#!/bin/bash

echo "Ip adress of host at $(hostname -i) "

jupyter lab\
	--port=8888\
	--no-browser\
	--ip=0.0.0.0\
	--allow-root
