#!/bin/bash

#check if there is a /build and /devel in the current PWD
# if [ -f devel/.catkin ]; then
# echo "Starting from Catkin Workspace: $PWD, preparing it's ROS_PACKAGE_PATH."

# # If you start this script inside a catkin workspace, it will make that workspace available in the projects src folder
# sed -i 's/;\/projects\/src//' devel/.catkin
# echo -n "`cat devel/.catkin`;/projects/src" > devel/.catkin
# fi

docker run -iPt \
    --rm \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
    --device=/dev/dri:/dev/dri \
    --env="DISPLAY=$DISPLAY" \
    --env="XAUTHORITY=$XAUTHORITY" \
    --volume="$XAUTHORITY:$XAUTHORITY" \
    --volume="$PWD:/projects" \
    --name="ros_melodic_desktop_px4" \
    ros_melodic_desktop_px4 \
    bash
