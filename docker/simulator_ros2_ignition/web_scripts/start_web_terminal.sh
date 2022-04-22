#!/bin/sh
echo $SSH_PUBLIC_KEY > ~/.ssh/authorized_keys &
/usr/sbin/sshd -D &
. /usr/local/nvm/nvm.sh
nvm use 14
wetty --conf /web_scripts/config.json --ssh-config /etc/ssh/ssh_config --command 'cd / && bash'
