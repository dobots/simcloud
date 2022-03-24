FROM osrf/ros:foxy-desktop

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# Ensure bin/sh (default shell) is set to bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Basic installs for Image:
## (Optional) Update ros packages to the latest version
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y less nano wget psmisc zip build-essential git mercurial vim
# mesa packages for non-nvidia users
RUN apt-get install -y libgl1-mesa-glx libgl1-mesa-dri

# Gazebo (Optional)
RUN apt-get install -y gazebo11 libgazebo11-dev ros-foxy-gazebo-ros-pkgs

## source ROS:
### Fix entrypoint.sh file
RUN sed -i 's/set -e//' /ros_entrypoint.sh

## setup source folder:
RUN mkdir /source_scripts
RUN echo 'for i in /source_scripts/*; do source $i; done' >> /source_me.bash
RUN echo 'echo "COLCON_PREFIX_PATH := $COLCON_PREFIX_PATH"' >> /source_me.bash
RUN echo 'source /source_me.bash' >> /root/.bashrc
## source ROS_DISTRO
RUN echo 'source "/opt/ros/foxy/setup.bash"' >> /source_scripts/0defaults
## source Gazebo:
RUN echo "source /usr/share/gazebo/setup.sh" >> /source_scripts/0defaults

WORKDIR /

# install rosbridge
RUN apt-get install ros-foxy-rosbridge-suite -y

### General ROS packages
RUN apt-get update && apt-get install -y ros-foxy-teleop-twist-keyboard ros-foxy-teleop-twist-joy  

### Install ROS1 noetic and rosbridge for bridge to webviz 
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt update -y && sudo apt install -y ros-noetic-ros-base && sudo apt install -y ros-noetic-rosbridge-server
RUN apt install -y ros-foxy-ros1-bridge

### GazeboWeb
#dependencies
WORKDIR /
EXPOSE 8080
RUN apt-get update && apt-get install -y libjansson-dev libboost-dev imagemagick libtinyxml-dev mercurial cmake build-essential libgts-dev

#instalation of nvm (older versions of nodejs and npm are required)
ENV NVM_DIR /usr/local/nvm
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
ENV NODE_VERSION v8.9.0
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefi $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
 
#add db of used models requirment of gzweb
COPY ./gzweb_model_db/ /gzweb_db/

RUN ln -s /usr/bin/python2.7 /usr/bin/python

#build of gzweb
RUN git clone https://github.com/osrf/gzweb
WORKDIR /gzweb
RUN git checkout gzweb_1.4.1
#Trying to fix null pointer segfault:
COPY ./gzbridge.patch /gzweb/gzbridge/
WORKDIR /gzweb/gzbridge
RUN patch -p0 < gzbridge.patch
WORKDIR /gzweb
RUN /bin/bash -c "source /source_me.bash && export GAZEBO_MODEL_PATH=/gzweb_db:$GAZEBO_MODEL_PATH && npm run deploy --- -m local"
RUN sed -i 's|ws://|wss://|' http/client/gz3d.gui.js
RUN sed -i "s|'http://'|'https://'|" http/client/gz3d.gui.js

#ensure the right entry point for the docker container
WORKDIR /



## WebViz
WORKDIR /
RUN git clone https://github.com/cruise-automation/webviz.git
WORKDIR webviz
ENV NODE_VERSION v14.16.1
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
RUN npm i -g npm@latest
RUN npm run bootstrap
RUN npm run build-static-webviz
RUN sed -i 's/http-server __static_webviz__/http-server --port 8081 __static_webviz__/g' ./package.json
WORKDIR /

#install wetty
ENV NVM_DIR /usr/local/nvm
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
ENV NODE_VERSION v14.16.1
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
RUN npm install -g yarn
RUN yarn global add wetty@2.0.3
EXPOSE 3000
COPY ./web_scripts/ /web_scripts/
RUN cd web_scripts && chmod +x start_web_terminal.sh start_gzweb.sh start_webviz.sh

# install Foxglove
#RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
#RUN apt install git-lfs
#RUN git clone https://github.com/foxglove/studio.git
#WORKDIR studio 
#RUN git lfs pull
#RUN apt update -y && yarn install
#WORKDIR /
 
#enable ssh into the container
RUN apt-get update && apt-get install -y openssh-server sshpass
RUN service ssh start
EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]

WORKDIR /

# set root pw for wetty - (LUDO) Is this really necessary? Open passwords in Github?
RUN echo "root:dobots_rocks" | chpasswd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# Add nvm to bashrc as well:
RUN echo "export NVM_DIR="/usr/local/nvm"" >> /root/.bashrc
RUN echo "[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"" >> /root/.bashrc

# clean up the terminal for wetty - (LUDO) This is nasty! Don't navigate on arbitrary bash startups!
#RUN echo "cd /" >> /root/.bashrc
# making sure that gzweb does not crash on start up
RUN echo "export GAZEBO_MODEL_DATABASE_URI=countvoncount.math" >> /root/.bashrc
#RUN echo "clear" >> /root/.bashrc
# add style to wetty
#RUN echo "export PS1='ASIMOVO:\W '" >> /root/.bashrc

# Add ros_packages and UAV sourcing to bashrc as well:
RUN mkdir /our_ros_packages; cd /our_ros_packages; mkdir src
RUN cd /our_ros_packages/src; git clone --single-branch --branch foxy https://github.com/husarion/rosbot_description.git; 
RUN source /opt/ros/foxy/setup.bash; cd /our_ros_packages; rosdep install --from-paths src --ignore-src -r -y; colcon build; source /source_me.bash
RUN /bin/bash -c 'source /source_me.bash'
RUN echo '. /our_ros_packages/install/setup.sh' >> /source_scripts/1system
RUN cp -r /gzweb_db/rosbot_description /gzweb/http/client/assets/
# Add gzweb package modifications
COPY ./rosbot_files/ /our_ros_packages/rosbot_files/
RUN cp /our_ros_packages/rosbot_files/* /our_ros_packages/install/rosbot_description/share/rosbot_description/ 
RUN sed -i 's|/models/rosbot|/rosbot|' /our_ros_packages/install/rosbot_description/share/rosbot_description/launch/rosbot_spawn.launch.py


#Install Pip and Jupyter
RUN sudo apt-get -y install python3-pip 
RUN pip3 install jupyter jupyterlab jupytext jupyter-book
RUN pip3 install --upgrade --no-deps --force-reinstall jupyterlab-myst


