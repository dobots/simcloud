#!/bin/sh
. /usr/local/nvm/nvm.sh
nvm use 14
wetty --conf web_terminal_scripts/config.json --ssh-config /etc/ssh/ssh_config
