#!/bin/bash -l

export NODE_VERSION=v8.9.0
source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION
export NODE_PATH=$NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
export PATH=$NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

cd /gzweb
npm start

