#!/bin/sh
/usr/sbin/sshd -D &
. /usr/local/nvm/nvm.sh
nvm use 14
wetty --conf /web_scripts/config.json --ssh-config /etc/ssh/ssh_config --command 'cd / && bash'
