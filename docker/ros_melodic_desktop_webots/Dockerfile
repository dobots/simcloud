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

###### Install WeBots 
WORKDIR /
# Disable dpkg/gdebi interactive dialogs
ENV DEBIAN_FRONTEND=noninteractive

# Determine Webots version to be used and set default argument
ARG WEBOTS_VERSION=R2021a
ARG WEBOTS_PACKAGE_PREFIX=_ubuntu-18.04

# Install Webots runtime dependencies
RUN apt-get install -y ffmpeg g++ make libavcodec-extra libglu1-mesa libxkbcommon-x11-dev execstack libusb-dev libxcb-keysyms1 libxcb-image0 libxcb-icccm4 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcomposite-dev libxtst6 libnss3
# Install X virtual framebuffer to be able to use Webots without GPU and GUI (e.g. CI)
RUN apt-get install -y xvfb

# Install Webots
WORKDIR /
RUN wget https://github.com/cyberbotics/webots/releases/download/$WEBOTS_VERSION/webots-$WEBOTS_VERSION-x86-64$WEBOTS_PACKAGE_PREFIX.tar.bz2
RUN tar xjf webots-*.tar.bz2 && rm webots-*.tar.bz2
ENV QTWEBENGINE_DISABLE_SANDBOX=1
ENV WEBOTS_HOME /webots
ENV PATH /webots:${PATH}

# Install Webots-ROS package
RUN apt-get install -y ros-melodic-webots-ros

######

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
# (Optional) Add ros_packages and UAV sourcing to bashrc as well:
# RUN echo ". /projects/ros_packages/devel/setup.bash" >> ~/.bashrc
# RUN echo ". \$(rospack find uav)/scripts/init_uav_px4.sh > /dev/null" >> ~/.bashrc

# Ensure image runs bash
CMD ["bash"]
