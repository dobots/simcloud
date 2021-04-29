#!/bin/bash

# run container (detached)
docker run -iPt -d \
    --rm \
    -v /dev/bus/usb:/dev/bus/usb \
    -v /dev/input:/dev/input \
    --device-cgroup-rule 'a 13:* rwm' \
    --device-cgroup-rule 'a 189:* rwm' \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$XAUTHORITY:$XAUTHORITY" \
    --env="XAUTHORITY=$XAUTHORITY" \
    --volume="/home/sjauhri/DoBots_WS/simcloud:/projects" \ # Replace with your simcloud repo path!!!
    --runtime=nvidia \
    --name="ros_melodic_desktop_px4" \
    ros_melodic_desktop_px4

# run simulation
docker exec \
    ros_melodic_desktop_px4 \
    bash -i -c \
    'cd /projects/ros_packages/ && catkin_make && source ~/.bashrc && roslaunch uav bringup.launch' # Command to run