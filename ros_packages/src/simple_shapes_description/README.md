﻿## Simple shapes environment description

ROS package, which includes the mesh files, sdf description, world description and a launch file to launch  a world with some simple shapes

To launch the world file include the following in your launch file:

    <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="$(find simple_shapes_description)/worlds/simple_shapes.world"/>
    </include>

or run the launch file:

    roslaunch simple_shapes_description simple_shapes_world.launch

## Edit the package.xml file

It is desirable to make the codes easily portable and therefore all the mesh files should be stored in this package instead of the .gazebo/models folder. This can be achieved by editing the package.xml file in the current package to add it to the gazebo model path:

    <export>
    <!-- gazebo_ros_paths_plugin automatically adds these to
        GAZEBO_PLUGIN_PATH and GAZEBO_MODEL_PATH when you do this export inside
        the package.xml file. -->
    <gazebo_ros 
        gazebo_plugin_path="${prefix}/lib"
        gazebo_model_path="${prefix}/.." /> 
    </export>



