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

# ROS #
## (Optional) Update ros packages to the latest version
# RUN apt-get upgrade -y

## sourcing
RUN echo ". /ros_entrypoint.sh" >> ~/.bashrc
RUN echo ". /usr/share/gazebo/setup.sh" >> ~/.bashrc

## Fix entrypoint.sh file
RUN sed -i 's/set -e//' /ros_entrypoint.sh

## Additional installs (Optional)
### General packages:
RUN apt-get install -y ros-melodic-teleop-twist-keyboard ros-melodic-move-base ros-melodic-map-server ros-melodic-gmapping ros-melodic-hector-slam

### PX4 installation
#### Initial setup:
RUN apt-get remove modemmanager -y
RUN apt-get install -y cmake genromfs ninja-build xxd vim-gtk exiftool
RUN apt-get install -y python3-pip
RUN pip3 install empy toml numpy pyros-genmsg jinja2 packaging pyserial pyyaml
# gstreamer for PX4-AutoPilot and QGroundControl
RUN apt-get install -y gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl libgstreamer-plugins-base1.0-dev
# (Optional) RUN apt-get install -y qtcreator

#### Install FastRTPS 1.7.1 and FastCDR-1.0.8
RUN wget https://www.eprosima.com/index.php/component/ars/repository/eprosima-fast-dds/eprosima-fast-rtps-1-7-2/eprosima_fastrtps-1-7-2-linux-tar-gz?format=raw -O eprosima_fastrtps-1-7-2-linux.tar.gz
RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz eProsima_FastRTPS-1.7.2-Linux
RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz requiredcomponents
RUN tar -xzf requiredcomponents/eProsima_FastCDR-1.0.8-Linux.tar.gz
RUN cd eProsima_FastCDR-1.0.8-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
RUN cd eProsima_FastRTPS-1.7.2-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
RUN rm -rf requiredcomponents eprosima_fastrtps-1-7-2-linux.tar.gz
#### Install MAVROS
# (Optional) RUN apt-get install -y python-rosinstall-generator python-catkin-tools
RUN apt-get install -y ros-melodic-mavros ros-melodic-mavros-extras
RUN wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh -O - | bash
#### Download and build PX4-Autopilot
RUN mkdir PX4
WORKDIR PX4
RUN git clone https://github.com/PX4/Firmware.git
WORKDIR /PX4/Firmware
RUN DONT_RUN=1 make px4_sitl gazebo
# TODO: Source Firmware and add to ROS PACKAGE PATH

### Install QGroundControl:
WORKDIR /
RUN mkdir QGroundControl
WORKDIR QGroundControl
RUN wget https://s3-us-west-2.amazonaws.com/qgroundcontrol/builds/master/QGroundControl.AppImage -O QGroundControl.AppImage
RUN apt-get install libarchive-tools && bsdtar xfp QGroundControl.AppImage
# Now you may run the app using ./QGroundControl/AppRun (As a non root user)

### GazeboWeb (TODO) (Optional):
WORKDIR /
# EXPOSE 8080
# RUN apt-get install -y nodejs libjansson-dev libboost-dev imagemagick libtinyxml-dev astyle
# RUN apt-get install -y ant openjdk-8-jdk openjdk-8-jre


# Ensure image runs bash
CMD ["bash"]