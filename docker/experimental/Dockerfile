FROM ros:melodic-ros-core as build
# 'desktop-full' includes gazebo9

# Relative static changes:
EXPOSE 8080 3000 22

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics
# Ensure bin/sh (default shell) is set to bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
### Fix entrypoint.sh file
RUN sed -i 's/set -e//' /ros_entrypoint.sh

# apt installs that aren't expected to change much and where it's not a problem if it's an older version in the image

# merge all apt-get calls into single operation for efficiency:
# gstreamer for PX4-AutoPilot and QGroundControl
RUN apt-get update -y && apt-get install -y --no-install-recommends apt-utils curl less nano wget psmisc zip build-essential git mercurial jstest-gtk cmake genromfs xxd vim-gtk exiftool python3-pip gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl libgstreamer-plugins-base1.0-dev libpcl1 nodejs libjansson-dev libboost-dev imagemagick libtinyxml-dev mercurial cmake build-essential libgts-dev astyle ant openjdk-8-jdk openjdk-8-jre libarchive-tools python-rosdep-modules python-rosdep python3-setuptools openssh-server sshpass modemmanager-  && rm -rf /var/lib/apt/lists/*
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN pip3 install wheel 
RUN pip3 install empy toml numpy pyros-genmsg jinja2 packaging pyserial pyyaml jsonschema kconfiglib
# (Optional) RUN apt-get install -y qtcreator

## setup source folder:
RUN mkdir /source_scripts
RUN echo 'for i in /source_scripts/*; do source $i; done' >> /source_me.bash
RUN echo 'echo "ROS_PACKAGE_PATH := $ROS_PACKAGE_PATH"' >> /source_me.bash
RUN echo 'source /source_me.bash' >> /root/.bashrc
## source ROS_DISTRO
RUN echo 'source "/opt/ros/$ROS_DISTRO/setup.bash"' >> /source_scripts/0defaults
## source Gazebo:
RUN echo "source /usr/share/gazebo/setup.sh" >> /source_scripts/0defaults

#instalation of nvm (older versions of nodejs and npm are required)
ENV NVM_DIR /usr/local/nvm
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
# Add nvm to bashrc as well:
RUN echo "export NVM_DIR="/usr/local/nvm"" >> /root/.bashrc
RUN echo "[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"" >> /root/.bashrc

### Install QGroundControl:
WORKDIR /
RUN mkdir QGroundControl
WORKDIR QGroundControl
RUN wget https://github.com/mavlink/qgroundcontrol/releases/download/v3.5.6/QGroundControl.AppImage
RUN bsdtar xfp QGroundControl.AppImage
# Now you may run the app using ./QGroundControl/qgroundcontrol-start.sh (As a non root user)



# Expensive builds
WORKDIR /
RUN apt-get update -y && apt-get install -y --no-install-recommends libgazebo9-dev ros-melodic-gazebo-dev ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros ros-melodic-mavros ros-melodic-mavros-extras ros-melodic-genpy ros-melodic-pcl-ros ros-melodic-octomap-* && rm -rf /var/lib/apt/lists/*

#add db of used models requirment of gzweb
COPY ./gzweb_model_db/ /gzweb_db/

#add copy of our webscripts:
COPY ./web_scripts/ /web_scripts/
RUN cd /web_scripts && chmod +x start_web_terminal.sh start_gzweb.sh start_webviz.sh

#### Clone and build PX4-Autopilot
RUN mkdir -p PX4/src
WORKDIR PX4

RUN git clone https://github.com/PX4/PX4-Autopilot.git Firmware
WORKDIR /PX4/Firmware
RUN git checkout v1.13.0-alpha1

# set default of 'RC loss exceptions' to offboard to enable offboard opperations without rc signal - required after px4 update 
RUN sed -i 's/PARAM_DEFINE_INT32(COM_RCL_EXCEPT, 0);/PARAM_DEFINE_INT32(COM_RCL_EXCEPT, 4);/g' /PX4/Firmware/src/modules/commander/commander_params.c
RUN sed -i '/interactive/s/true/false/' /PX4/Firmware/launch/px4.launch

RUN HEADLESS=1 DONT_RUN=1 make px4_sitl gazebo
WORKDIR /PX4/Firmware/build/px4_sitl_default/
RUN sed -i '/CPACK_PACKAGE_VERSION/s/CPACK_PACKAGE_VERSION "v/CPACK_PACKAGE_VERSION "/' /PX4/Firmware/build/px4_sitl_default/CPackConfig.cmake
RUN make; cpack -G DEB; dpkg -i *.deb

#### (Optional) Clone and build PX4-Avoidance for collision avoidance
# Create catkin workspace for PX4
WORKDIR /PX4/src
RUN git clone https://github.com/dobots/PX4-Avoidance.git
RUN rm -f CMakeLists.txt; source /source_me.bash; catkin_init_workspace
RUN /bin/bash -c 'source /source_me.bash; catkin_make -C /PX4'

# Source PX4 Avoidance catkin workspace in bashrc (More later, when our ros_packages are included)
RUN echo 'export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:/PX4/src/avoidance/avoidance/sim/models:/PX4/src/avoidance/avoidance/sim/worlds' >> /source_scripts/1system
RUN echo 'source /PX4/devel/setup.bash' >> /source_scripts/1system

# Give all users permission to use PX4 catkin workspace
#RUN chmod -R a+rw /PX4/
#RUN chmod -R a+rwx /PX4/build/
#RUN chmod -R a+rwx /PX4/devel/
#RUN chmod -R a+rwx /PX4/src/

WORKDIR /
RUN rm -rf /PX4/Firmware

#### (Optional) Install FastRTPS 1.7.1 and FastCDR-1.0.8
# RUN wget https://www.eprosima.com/index.php/component/ars/repository/eprosima-fast-dds/eprosima-fast-rtps-1-7-2/eprosima_fastrtps-1-7-2-linux-tar-gz?format=raw -O eprosima_fastrtps-1-7-2-linux.tar.gz
# RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz eProsima_FastRTPS-1.7.2-Linux
# RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz requiredcomponents
# RUN tar -xzf requiredcomponents/eProsima_FastCDR-1.0.8-Linux.tar.gz
# RUN cd eProsima_FastCDR-1.0.8-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
# RUN cd eProsima_FastRTPS-1.7.2-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
# RUN rm -rf requiredcomponents eprosima_fastrtps-1-7-2-linux.tar.gz

#build of gzweb
ENV NODE_VERSION v8.9.0
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

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
WORKDIR /

RUN wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh -O - | bash

### WebViz
WORKDIR /
RUN git clone https://github.com/cruise-automation/webviz.git
WORKDIR webviz
ENV NODE_VERSION v14.16.1
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
RUN npm run bootstrap
RUN npm run build-static-webviz
RUN sed -i 's/http-server __static_webviz__/http-server --port 8081 __static_webviz__/g' ./package.json
WORKDIR /

#install wetty
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
ENV NODE_VERSION v14.16.1
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
RUN npm install -g yarn
RUN yarn global add wetty@2.0.3


# Expected to change more often:
RUN apt-get update -y && apt-get dist-upgrade -y  && rm -rf /var/lib/apt/lists/*
## General ROS packages
RUN apt-get update -y && apt-get install -y ros-melodic-teleop-twist-keyboard ros-melodic-teleop-twist-joy ros-melodic-map-server ros-melodic-amcl ros-melodic-gmapping ros-melodic-jsk-rviz-plugins ros-melodic-gazebo-ros ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control ros-melodic-move-base ros-melodic-global-planner ros-melodic-teb-local-planner ros-melodic-position-controllers ros-melodic-effort-controllers ros-melodic-joint-state-controller  && rm -rf /var/lib/apt/lists/*
## mesa packages for non-nvidia users
RUN apt-get update -y && apt-get install -y --no-install-recommends libgl1-mesa-glx libgl1-mesa-dri   && rm -rf /var/lib/apt/lists/*

# install rosbridge
RUN apt-get install ros-melodic-rosbridge-suite -y


WORKDIR /

#enable ssh into the container
RUN service ssh start
CMD ["/usr/sbin/sshd","-D"]

# set root pw for wetty - (LUDO) Is this really necessary? Open passwords in Github?
RUN echo "root:dobots_rocks" | chpasswd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# clean up the terminal for wetty - (LUDO) This is nasty! Don't navigate on arbitrary bash startups!
RUN echo "cd /" >> /root/.bashrc

# making sure that gzweb does not crash on start up
RUN echo "export GAZEBO_MODEL_DATABASE_URI=countvoncount.math" >> /root/.bashrc

# Add ros_packages and UAV sourcing to bashrc as well:
COPY ./ros_packages /our_ros_packages
RUN cd /our_ros_packages; rm -rf build devel
RUN cd /our_ros_packages/src; rm -f CMakeLists.txt; source /source_me.bash; catkin_init_workspace
RUN /bin/bash -c 'source /source_me.bash; catkin_make -C /our_ros_packages'
RUN echo '. /our_ros_packages/devel/setup.bash' >> /source_scripts/1system
RUN echo '. $(rospack find uav)/scripts/init_uav_px4_deb.sh' >> /source_scripts/999px4Firmware

# Finally double-check if there are any updates:
RUN apt-get update -y && apt-get dist-upgrade -y && rm -rf /var/lib/apt/lists/*

# Ensure image runs bash - (BART?) UPDATE is disabled due to the web terminal
#CMD ["bash"]

#Now drop history and cleanup:
FROM scratch

COPY --from=build / /
WORKDIR /

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

CMD ["/usr/sbin/sshd","-D"]
# Ensure image runs bash - (BART?) UPDATE is disabled due to the web terminal
#CMD ["bash"]

ENV ROS_DISTRO melodic
ENV NVM_DIR /usr/local/nvm
EXPOSE 8080 3000 22


