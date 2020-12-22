FROM osrf/ros:melodic-desktop-full

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics


# Prepare/extend image to be a useful development environment
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get -y update && apt-get remove modemmanager -y
RUN apt-get -y update && apt-get install -y apt-utils build-essential psmisc vim-gtk
RUN apt-get -y update && apt-get install -y less nano nodejs libjansson-dev libboost-dev imagemagick libtinyxml-dev mercurial git genromfs ninja-build exiftool astyle xxd python-argparse python-toml python-pip python-rosinstall-generator python-catkin-tools
RUN apt-get -y update && apt-get install -y ant openjdk-8-jdk openjdk-8-jre
RUN apt-get -y update && apt-get install -y ros-melodic-navigation ros-melodic-hector-slam ros-melodic-teb-local-planner ros-melodic-teleop-twist-keyboard ros-melodic-hector-gazebo-plugins
RUN apt-get -y update && apt-get install -y geographiclib-tools gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl libgstreamer-plugins-base1.0-dev


# Ensure bin/sh (default shell) is set to bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# apt update
RUN apt-get update -y && apt-get install -y less nano

# ROS sourcing
RUN echo ". /ros_entrypoint.sh" >> ~/.bashrc
# Fix entrypoint.sh file
RUN sed -i 's/set -e//' /ros_entrypoint.sh


# Update and install Python tools
RUN apt-get -y update && apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install pandas jinja2 pyserial pyyaml pyulog 
RUN pip3 install --upgrade pip
RUN pip3 install toml empy numpy pyros-genmsg jinja2 packaging pyserial pyyaml pyulog

# Download and build MAVROS:
COPY build_mavros.sh .
RUN /build_mavros.sh

# Download PX4 simulator
RUN mkdir PX4
WORKDIR PX4
RUN git clone https://github.com/PX4/Firmware.git

WORKDIR /
# Install FastRTPS 1.7.1 and FastCDR-1.0.8 (Dependencies of the PX4 Simulator)
RUN wget https://www.eprosima.com/index.php/component/ars/repository/eprosima-fast-dds/eprosima-fast-rtps-1-7-2/eprosima_fastrtps-1-7-2-linux-tar-gz?format=raw -O eprosima_fastrtps-1-7-2-linux.tar.gz
RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz eProsima_FastRTPS-1.7.2-Linux
RUN tar -xzf eprosima_fastrtps-1-7-2-linux.tar.gz requiredcomponents
RUN tar -xzf requiredcomponents/eProsima_FastCDR-1.0.8-Linux.tar.gz

RUN cd eProsima_FastCDR-1.0.8-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
RUN cd eProsima_FastRTPS-1.7.2-Linux && ./configure --libdir=/usr/lib && make -j4 && make install
RUN rm -rf requiredcomponents eprosima_fastrtps-1-7-2-linux.tar.gz

# Build PX4 simulator
WORKDIR /PX4/Firmware
RUN DONT_RUN=1 make px4_sitl gazebo

# Install QGroundcontrol
WORKDIR /root/
RUN wget https://s3-us-west-2.amazonaws.com/qgroundcontrol/latest/QGroundControl.AppImage -O QGroundControl.AppImage
RUN chmod +x ./QGroundControl.AppImage
#RUN ./QGroundControl.AppImage --appimage-extract-and-run

# Install drone tooling for ROS
RUN apt-get -y update && apt-get install -y ros-melodic-ar-track-alvar ros-melodic-jsk-rviz-plugins
RUN catkin_ws/src/mavros/mavros/scripts/install_geographiclib_datasets.sh


# Deploy Gazebo models for GZWEB (Needs filtering, otherwise extreme long duration)
WORKDIR /
RUN git clone https://github.com/osrf/gzweb.git
#WORKDIR /gzweb
#RUN  . /usr/share/gazebo/setup.sh; ./deploy.sh -m

WORKDIR /
# Copy my own demo scripts:
#COPY demo_setup.sh .
#COPY launch_demo_script.sh .
#COPY launch_demo.sh .





RUN apt-get -y update && apt-get -y install libgl1-mesa-glx libgl1-mesa-dri
RUN rm -rf /var/lib/apt/lists/*

# Normal init
EXPOSE 8080
CMD ["bash"]

