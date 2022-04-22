#!/bin/bash

#bluetooth setup
#service dbus start
#bluetoothd &

#check if there is a /build and /devel in the current PWD
# if [ -f devel/.catkin ]; then
# echo "Starting from Catkin Workspace: $PWD, preparing it's ROS_PACKAGE_PATH."

# # If you start this script inside a catkin workspace, it will make that workspace available in the projects src folder
# sed -i 's/;\/projects\/src//' devel/.catkin
# echo -n "`cat devel/.catkin`;/projects/src" > devel/.catkin
# fi


docker run -iPt \
    --rm \
    -d \
    -v /dev/bus/usb:/dev/bus/usb \
    -v /dev/input:/dev/input \
    -p 8001:8001 \
    -p 8080:8080 \
    -p 4000:4000 \
    -p 9002:9002 \
    -p 80:80 \
    -p 2222:22 \
    --device-cgroup-rule 'a 13:* rwm' \
    --device-cgroup-rule 'a 189:* rwm' \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$XAUTHORITY:$XAUTHORITY" \
    --env="XAUTHORITY=$XAUTHORITY" \
    --volume="$PWD:/projects" \
    --runtime=nvidia \
    --name="simulator_ros2_ignition" \
    simulator_ros2_ignition \
