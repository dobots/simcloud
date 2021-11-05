FROM ros:melodic-ros-core
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

#### Clone and build PX4-Autopilot
RUN mkdir -p PX4/src
WORKDIR PX4

RUN git clone https://github.com/PX4/PX4-Autopilot.git Firmware
# set default of 'RC loss exceptions' to offboard to enable offboard opperations without rc signal - required after px4 update 
RUN sed -i 's/PARAM_DEFINE_INT32(COM_RCL_EXCEPT, 0);/PARAM_DEFINE_INT32(COM_RCL_EXCEPT, 4);/g' /PX4/Firmware/src/modules/commander/commander_params.c
RUN sed -i '/interactive/s/true/false/' /PX4/Firmware/launch/px4.launch
WORKDIR /PX4/Firmware

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

WORKDIR /
RUN rm -rf /PX4/Firmware

RUN wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh -O - | bash

# Expected to change more often:
RUN apt-get update -y && apt-get dist-upgrade -y  && rm -rf /var/lib/apt/lists/*
## General ROS packages
RUN apt-get update -y && apt-get install -y ros-melodic-teleop-twist-keyboard ros-melodic-teleop-twist-joy ros-melodic-map-server ros-melodic-amcl ros-melodic-gmapping ros-melodic-jsk-rviz-plugins ros-melodic-gazebo-ros ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control ros-melodic-move-base ros-melodic-global-planner ros-melodic-teb-local-planner ros-melodic-position-controllers ros-melodic-effort-controllers ros-melodic-joint-state-controller  && rm -rf /var/lib/apt/lists/*
## mesa packages for non-nvidia users
RUN apt-get update -y && apt-get install -y --no-install-recommends libgl1-mesa-glx libgl1-mesa-dri   && rm -rf /var/lib/apt/lists/*
#install rvizweb

# Add ros_packages and UAV sourcing to bashrc as well:
COPY ./ros_packages /our_ros_packages
RUN cd /our_ros_packages; rm -rf build devel
RUN cd /our_ros_packages/src; rm -f CMakeLists.txt; source /source_me.bash; catkin_init_workspace
RUN /bin/bash -c 'source /source_me.bash; catkin_make -C /our_ros_packages'
RUN echo '. /our_ros_packages/devel/setup.bash' >> /source_scripts/1system
RUN echo '. $(rospack find uav)/scripts/init_uav_px4_deb.sh' >> /source_scripts/999px4Firmware

# Finally double-check if there are any updates:
RUN apt-get update -y && apt-get dist-upgrade -y && rm -rf /var/lib/apt/lists/*

# Ensure image runs bash
CMD ["bash"]


