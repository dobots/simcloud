FROM osrf/ros:melodic-desktop-full
# 'desktop-full' includes gazebo9


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
RUN apt-get install -y less nano wget psmisc zip build-essential git mercurial
# mesa packages for non-nvidia users
RUN apt-get install -y libgl1-mesa-glx libgl1-mesa-dri

# install joystick package
RUN apt-get install -y jstest-gtk

# install bluetooth packages
#RUN apt-get install -y libbluetooth-dev bluez bluetooth

## source ROS:
### Fix entrypoint.sh file
RUN sed -i 's/set -e//' /ros_entrypoint.sh

## setup source folder:
RUN mkdir /source_scripts
RUN echo 'for i in /source_scripts/*; do source $i; done' >> /source_me.bash
RUN echo 'echo "ROS_PACKAGE_PATH := $ROS_PACKAGE_PATH"' >> /source_me.bash
RUN echo 'source /source_me.bash' >> /root/.bashrc
## source ROS_DISTRO
RUN echo 'source "/opt/ros/melodic/setup.bash"' >> /source_scripts/0defaults
## source Gazebo:
RUN echo "source /usr/share/gazebo/setup.sh" >> /source_scripts/0defaults

## Additional installs:

WORKDIR /

### General ROS packages
RUN apt-get update && apt-get install -y ros-melodic-teleop-twist-keyboard ros-melodic-teleop-twist-joy ros-melodic-map-server ros-melodic-amcl ros-melodic-gmapping ros-melodic-jsk-rviz-plugins
RUN apt-get install -y ros-melodic-move-base ros-melodic-global-planner ros-melodic-teb-local-planner

# install rosbridge
RUN apt-get install ros-melodic-rosbridge-suite -y


### PX4 installation
#### Initial setup:
RUN apt-get remove modemmanager -y
RUN apt-get install -y cmake genromfs xxd vim-gtk exiftool
RUN apt-get install -y python3-pip
RUN pip3 install empy toml numpy pyros-genmsg jinja2 packaging pyserial pyyaml jsonschema kconfiglib
# gstreamer for PX4-AutoPilot and QGroundControl
RUN apt-get install -y gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl libgstreamer-plugins-base1.0-dev
# (Optional) RUN apt-get install -y qtcreator

#### (Optional) Install FastRTPS 1.7.1 and FastCDR-1.0.8
# RUN wget https://www.eprosima.com/index.php/component/ars/repository/eprosima-fast-dds/eprosima-fast-rtps-1-7-2/eprosima_fastrtps-1-7-2-linux-tar-gz?format=raw -O eprosima_fastrtps-1-7-2-linux.tar.gz
# RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz eProsima_FastRTPS-1.7.2-Linux
# RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz requiredcomponents
# RUN tar -xzf requiredcomponents/eProsima_FastCDR-1.0.8-Linux.tar.gz
# RUN cd eProsima_FastCDR-1.0.8-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
# RUN cd eProsima_FastRTPS-1.7.2-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
# RUN rm -rf requiredcomponents eprosima_fastrtps-1-7-2-linux.tar.gz

#### Install MAVROS
# (Optional) RUN apt-get install -y python-rosinstall-generator python-catkin-tools
RUN apt-get install -y ros-melodic-mavros ros-melodic-mavros-extras ros-melodic-genpy
RUN wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh -O - | bash

#### Clone and build PX4-Autopilot
RUN mkdir PX4
WORKDIR PX4

RUN git clone https://github.com/PX4/PX4-Autopilot.git Firmware
# set default of 'RC loss exceptions' to offboard to enable offboard opperations without rc signal - required after px4 update 
WORKDIR /PX4/Firmware
RUN git checkout v1.12.3

RUN sed -i 's/PARAM_DEFINE_INT32(COM_RCL_EXCEPT, 0);/PARAM_DEFINE_INT32(COM_RCL_EXCEPT, 4);/g' /PX4/Firmware/src/modules/commander/commander_params.c
RUN sed -i '/interactive/s/true/false/' /PX4/Firmware/launch/px4.launch

RUN HEADLESS=1 DONT_RUN=1 make px4_sitl gazebo

#### (Optional) Clone and build PX4-Avoidance for collision avoidance
RUN apt update && apt-get install -y libpcl1 ros-melodic-octomap-*
# Create catkin workspace for PX4
WORKDIR /PX4
RUN mkdir src
WORKDIR /PX4/src
RUN git clone https://github.com/dobots/PX4-Avoidance.git
RUN rm -f CMakeLists.txt; source /source_me.bash; catkin_init_workspace
RUN /bin/bash -c 'source /source_me.bash; catkin_make -C /PX4'

# Source PX4 catkin workspace in bashrc (More later, when our ros_packages are included)
RUN echo 'export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:/PX4/src/avoidance/avoidance/sim/models:/PX4/src/avoidance/avoidance/sim/worlds' >> /source_scripts/1system
RUN echo 'source /PX4/devel/setup.bash' >> /source_scripts/1system

# Give all users permission to use PX4 catkin workspace
RUN chmod -R a+rw /PX4/
RUN chmod -R a+rwx /PX4/build/
RUN chmod -R a+rwx /PX4/devel/
RUN chmod -R a+rwx /PX4/src/

### Install QGroundControl:
WORKDIR /
RUN apt-get update
RUN mkdir QGroundControl
WORKDIR QGroundControl
RUN wget https://github.com/mavlink/qgroundcontrol/releases/download/v3.5.6/QGroundControl.AppImage
RUN apt-get install -y libarchive-tools && bsdtar xfp QGroundControl.AppImage
# Now you may run the app using ./QGroundControl/qgroundcontrol-start.sh (As a non root user)

### GazeboWeb
#dependencies
WORKDIR /
EXPOSE 8080
RUN apt-get update && apt-get install -y libjansson-dev libboost-dev imagemagick libtinyxml-dev mercurial cmake build-essential libgts-dev

#instalation of nvm (older versions of nodejs and npm are required)
ENV NVM_DIR /usr/local/nvm
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
ENV NODE_VERSION v8.9.0
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

#add db of used models requirment of gzweb
COPY ./gzweb_model_db/ /gzweb_db/

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
#RUN /bin/bash -c "./updateGZ3D.sh" 
RUN sed -i 's|listen(port|listen(port, "0.0.0.0"|' gzbridge/server.js

### WebViz
#WORKDIR /
#RUN git clone https://github.com/cruise-automation/webviz.git
#WORKDIR webviz
#ENV NODE_VERSION v14.16.1
#RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
#ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
#ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
#RUN npm run bootstrap
#RUN npm run build-static-webviz
#RUN sed -i 's/http-server __static_webviz__/http-server --port 8081 __static_webviz__/g' ./package.json
#WORKDIR /

# install autoware
#RUN apt-get update
#RUN sudo apt install -y python-catkin-pkg python-rosdep ros-$ROS_DISTRO-catkin
#RUN sudo apt install -y python3-pip python3-colcon-common-extensions python3-setuptools python3-vcstool
#RUN pip3 install -U setuptools
#RUN mkdir -p autoware.ai/src
#WORKDIR /autoware.ai
#RUN wget -O autoware.ai.repos "https://raw.githubusercontent.com/Autoware-AI/autoware.ai/1.12.0/autoware.ai.repos"
#RUN vcs import src < autoware.ai.repos
#RUN source /opt/ros/melodic/setup.sh
#RUN source /ros_entrypoint.sh
#RUN rosdep update
#RUN rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
#RUN apt-get install -y ros-melodic-jsk-recognition-msgs ros-melodic-nmea-msgs ros-melodic-jsk-rviz-plugins ros-melodic-tvm-vendor ros-melodic-lanelet2-core ros-melodic-nmea-navsat-driver ros-melodic-lanelet2-io ros-melodic-lanelet2-maps ros-melodic-lanelet2-projection ros-melodic-lanelet2-routing  
#RUN . /opt/ros/melodic/setup.bash;  colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
#RUN echo 'source /autoware.ai/install/setup.bash' >> /source_scripts/1system
#WORKDIR / 

# install xvfb for headless rendering of the camera
RUN apt update && apt-get install -y xvfb

#ensure the right entry point for the docker container
WORKDIR /

#install velodyne packages
RUN apt-get update -y && apt-get install -y ros-melodic-velodyne-simulator

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

#enable ssh into the container
RUN apt-get update && apt-get install -y openssh-server sshpass
RUN service ssh start
EXPOSE 22
#CMD ["/usr/sbin/sshd","-D"]

# Create new simcloud user and simcloud group (id 1000) for running the container
#RUN addgroup --gid 1000 simcloud_group
#RUN adduser --disabled-password --gecos '' --uid 1000 --gid 1000 simcloud_user
# Allow simcloud_user to use sudo with no password
#RUN usermod -aG sudo simcloud_user
#RUN echo "simcloud_user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
#RUN  echo 'simcloud_user:dobots_rocks' | chpasswd
#USER simcloud_user

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
#RUN echo "export PS1='\e[0;36mASIMOVO:\w \e[m '" >> /root/.bashrc

# Add ros_packages and UAV sourcing to bashrc as well:
COPY ./ros_packages /our_ros_packages
RUN cd /our_ros_packages; rm -rf build devel
RUN cd /our_ros_packages/src; rm -f CMakeLists.txt; source /source_me.bash; catkin_init_workspace
RUN /bin/bash -c 'source /source_me.bash; catkin_make -C /our_ros_packages'
RUN echo '. /our_ros_packages/devel/setup.bash' >> /source_scripts/1system
RUN echo '. $(rospack find uav)/scripts/init_uav_px4.sh' >> /source_scripts/999px4Firmware

# start launch scripts
COPY ./test_launchfile.sh ./test_launchfile.sh
RUN chmod +x test_launchfile.sh
RUN mkdir -p ~/.ssh
CMD ["/web_scripts/start_web_terminal.sh"]

# Ensure image runs bash - (BART?) UPDATE is disabled due to the web terminal
#CMD ["bash"]
