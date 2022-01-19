# Collapsed fire station description

Contains the 3D model of a facotry hall. In addition it contains launch files to start the gazebo environment with one or multiple drones, or with a rover or without. It contains scripts to fly a predefined route.

The 3D model of a collapsed fire station is imported from the gazebo/models database.

### 1. Start the following launch file: 
```roslaunch factory_hall_description factory_hall.launch```
          
  If you would like to include the launch file in another launch file use the following code snippet in your launch file:
  
        <arg name="world_name" value="$(find factory_hall_description)/worlds/factory_hall.world"/>
      <include file="$(find gazebo_ros)/launch/empty_world.launch">
        <arg name="world_name" default="$(arg world_name)"/>
        <arg name="gui" default="$(arg gui)"/>
        <arg name="paused" default="$(arg paused)"/>
        <arg name="debug" default="$(arg debug)"/>
        <arg name="headless" default="$(arg headless)"/>
     </include>

    




