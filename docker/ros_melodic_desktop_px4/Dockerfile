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
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y less nano wget psmisc zip build-essential git mercurial
# mesa packages for non-nvidia users
RUN apt-get install -y libgl1-mesa-glx libgl1-mesa-dri

# ROS #
## (Optional) Update ros packages to the latest version
# RUN apt-get upgrade -y

## source ROS:
### Fix entrypoint.sh file
RUN sed -i 's/set -e//' /ros_entrypoint.sh
RUN echo ". /ros_entrypoint.sh" >> ~/.bashrc
## source Gazebo:
RUN echo ". /usr/share/gazebo/setup.sh" >> ~/.bashrc

## Additional installs:

### General ROS packages
RUN apt-get install -y ros-melodic-teleop-twist-keyboard ros-melodic-map-server ros-melodic-amcl ros-melodic-gmapping
RUN apt-get install -y ros-melodic-move-base ros-melodic-global-planner ros-melodic-teb-local-planner

### PX4 installation
#### Initial setup:
RUN apt-get remove modemmanager -y
RUN apt-get install -y cmake genromfs ninja-build xxd vim-gtk exiftool
RUN apt-get install -y python3-pip
RUN pip3 install empy toml numpy pyros-genmsg jinja2 packaging pyserial pyyaml
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
RUN git clone https://github.com/PX4/Firmware.git
WORKDIR /PX4/Firmware
RUN DONT_RUN=1 make px4_sitl gazebo
#### (Optional) Clone and build PX4-Avoidance for collision avoidance
RUN apt-get install -y libpcl1 ros-melodic-octomap-*
# Create catkin workspace for PX4
WORKDIR /PX4
RUN mkdir src
WORKDIR /PX4/src
RUN git clone https://github.com/PX4/avoidance.git
RUN /bin/bash -c '. /ros_entrypoint.sh; catkin_make -C /PX4'
# Source PX4 catkin workspace in bashrc (this ensures any other catkin workspaces are overlayed)
RUN echo $'# PX4 catkin workspace\n. /PX4/devel/setup.bash' >> ~/.bashrc
RUN echo $'export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:/PX4/src/avoidance/avoidance/sim/models:/PX4/src/avoidance/avoidance/sim/worlds\n' >> ~/.bashrc
# Give all users permission to use PX4 catkin workspace
RUN chmod -R a+rw /PX4/
RUN chmod -R a+rwx /PX4/build/
RUN chmod -R a+rwx /PX4/devel/
RUN chmod -R a+rwx /PX4/src/

### Install QGroundControl:
WORKDIR /
RUN mkdir QGroundControl
WORKDIR QGroundControl
RUN wget https://github.com/mavlink/qgroundcontrol/releases/download/v3.5.6/QGroundControl.AppImage
RUN apt-get install libarchive-tools && bsdtar xfp QGroundControl.AppImage
# Now you may run the app using ./QGroundControl/qgroundcontrol-start.sh (As a non root user)

### GazeboWeb (TODO) (Optional):
WORKDIR /
# EXPOSE 8080
# RUN apt-get install -y nodejs libjansson-dev libboost-dev imagemagick libtinyxml-dev astyle
# RUN apt-get install -y ant openjdk-8-jdk openjdk-8-jre

# Create new simcloud user and simcloud group (id 1000) for running the container
RUN addgroup --gid 1000 simcloud_group
RUN adduser --disabled-password --gecos '' --uid 1000 --gid 1000 simcloud_user
# Allow simcloud_user to use sudo with no password
RUN usermod -aG sudo simcloud_user
RUN echo "simcloud_user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER simcloud_user
## source ROS in bashrc for new user as well:
RUN echo ". /ros_entrypoint.sh" >> ~/.bashrc
## source Gazebo in bashrc:
RUN echo ". /usr/share/gazebo/setup.sh" >> ~/.bashrc
## source PX4 workspace in bashrc (this ensures any other catkin workspaces are overlayed):
RUN echo $'# PX4 catkin workspace\n. /PX4/devel/setup.bash' >> ~/.bashrc
RUN echo $'export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:/PX4/src/avoidance/avoidance/sim/models:/PX4/src/avoidance/avoidance/sim/worlds\n' >> ~/.bashrc
# (Optional) Add ros_packages and UAV sourcing to bashrc as well:
RUN echo ". /projects/ros_packages/devel/setup.bash" >> ~/.bashrc
RUN echo ". \$(rospack find uav)/scripts/init_uav_px4.sh > /dev/null" >> ~/.bashrc

# Ensure image runs bash
CMD ["bash"]