# Collapsed fire station description

Contains the 3D model of a collapsed fire station. In addition it contains launch files to start the gazebo environment with one or multiple drones, or with a rover or without. It contains scripts to fly a predefined route.

The 3D model of a collapsed fire station is imported from the gazebo/models database.

## Recommendations
If you haven't already finished the uav_workshop then we highly recommend to start with that.
Link to the drive folder with the raw code:[uav_workshop code](https://drive.google.com/drive/u/1/folders/1r3_Vf3Hlmav1xrZ7PRq1n7VgyLbzqOfC) 
Link to the tutorial: [uav workshop detailed guide](https://docs.google.com/document/d/1O4NJ3k8LbmTfkDLj4547qizohJDqM3KzZNpjvS4Yppc/edit) or [github_based version of the guide](https://github.com/dobots/uav_workshop/blob/master/README.md)

## Dependencies

 - uav package
	 - includes the UAV model and its config files
	 - it can be found in this repository as well
	 - or if you have followed the uav_workshop tutorial it should be already in your catkin folder
	 
 - px4 package 
	 - it was used during the UAV workshop as well
	 - use the following document to install: [uav workshop detailed guide ](https://docs.google.com/document/d/1O4NJ3k8LbmTfkDLj4547qizohJDqM3KzZNpjvS4Yppc/edit) or the [github_based version of the guide](https://github.com/dobots/uav_workshop/blob/master/README.md)
	 - or go the the official website: [Install and build PX4](https://dev.px4.io/v1.9.0/en/setup/dev_env_linux_ubuntu.html)
	 
 - rover_description package
	 - needed to spawn a rover
	 - it is included in this repository

## Launch one UAV in the environment


### 1. Start the following launch file: 
```roslaunch fire_station_description bringup_uav.launch```
      
The launch file will  look for the px4 package and the uav_workshop package to set up a UAV in the environment.
	In addition, it will call the start_gazebo_uav_world.launch file, which calls the 3D environment and sets the position of the UAV and spawns it. 


### 2. Start your script to fly on a predefined path:

```rosrun fire_station_description FLYinCollapsedFireStation.py```


### 3. Start the QGroundcontrol to Arm and Offboard the UAV:

```./QGroundcontrol```
    
    
    
  If you would like to include the launch file in another launch file use the following code snippet in your launch file:
  
        <arg name="world_name" value="$(find fire_station_description)/worlds/fire_station.world"/>
      <include file="$(find gazebo_ros)/launch/empty_world.launch">
        <arg name="world_name" default="$(arg world_name)"/>
        <arg name="gui" default="$(arg gui)"/>
        <arg name="paused" default="$(arg paused)"/>
        <arg name="debug" default="$(arg debug)"/>
        <arg name="headless" default="$(arg headless)"/>
     </include>



## Launch one UAV on top of a rover in the environment


### 1. Start the following launch file:

```roslaunch fire_station_description bringup_uav_rover.launch```
      
It will call the start_gazebo_uav_world.launch file, which calls the 3D environment and sets the position of the UAV and the rover. 


### 2. Start your script to fly on a predefined path:

```rosrun fire_station_description FLYinCollapsedFireStation_rover.py```
	    
	    
	    
### 3. 	Start the teleop:
				
```rosrun teleop_twist_keyboard teleop_twist_keyboard.py```
				
I usually decrease the default velocity, especially the angular one to make it easier to control.


### 4. Move with the rover forward until you reach the stairs. Then start the QGroundcontrol.


### 5. Start the QGroundcontrol to Arm and Offboard the UAV:

 ``` ./QGroundcontrol```
    
   

 
## Launch multiple UAVs on top of a rover in the environment
![multiple_uav.png](https://github.com/dobots/drones/blob/master/images/multiple_uav.png)

### 1. Start the following launch file to spawn the house and the rover:

```roslaunch fire_station_description bringup_multi_uav_rover.launch```
      

### 2. Launch the second launch file to spawn multiple UAVs in the envrionment:

```roslaunch fire_station_description spawn_multi_uav.launch```

**This launch file should be started after the rover appeared in the environment. If this launch file is included in the 1. launch file, then sometimes the rover is spawned on top of an UAV!!**

The ```spawn_multi_uav.launch``` file sets the parameters for each UAV and then calls the ```single_vehicle_spawn.launch``` file to spawn the UAV in the envrionment.

To add more UAVs (up to 10) you need to:

- Increase the id

- Change the name space

- Set the FCU to default="udp://:14540+id@localhost:14550+id"

- Set the malink_udp_port to 14560+id) 
  
The ```single_vehicle_spawn.launch``` file instead of the original urdf (px4/Tools/sitl_gazebo/models/rotors_description/urdf/iris_base.xacro) description can be edited to load the description located in the uav/gazebo_model/models/iris_camera/ folder instead of uav/gazebo_model/models/iris_camera/.
**It is an important difference, since in that folder a camera is added to the iris model of the UAV!**


### 4. Start your script to fly on a predefined path:

```rosrun fire_station_description FLYinCollapsedFireStation_2uavs.py```
	    
	    
### 5. 	Start the teleop:
				
```rosrun teleop_twist_keyboard teleop_twist_keyboard.py```
				
I usually decrease the default velocity, especially the angular one to make it easier to control.


### 6. Move with the rover forward until you reach the stairs. Then start the QGroundcontrol.


### 7. Start the QGroundcontrol to Arm and Offboard the UAV:

 ``` ./QGroundcontrol```
 
 From the drop-down menu at the top you can choose which UAV would you like to control.
![q_dropdown.png](https://github.com/dobots/drones/blob/master/images/q_dropdown.png)

### Comments on spawning multiple UAVs###


The PX4 package provides a launch file to spawn multiple UAVS (without camera) in an empty environment. The above described launch files are based on that launch file.

To run the original launch file:

```roslaunch px4 multi_uav_mavros_sitl.launch ```

   
  
## Make the camera follow the UAV

Include in the .world file the following:

        <!-- camera to follow the uav-->
        <!-- <gui fullscreen='0'>
        <camera name="user_camera">
        <track_visual>
          <name>iris_camera</name>
          <static>false</static>
          <min_dist>1.0</min_dist>
          <max_dist>2.0</max_dist>
          <use_model_frame>true</use_model_frame>
          <xyz>-1.0 0 0</xyz>
          <inherit_yaw>true</inherit_yaw>
        </track_visual>
    </camera>
</gui>

To quit the model following mode press Esc.





## Creating a UAV package with different 3D model

1. Include the 3D model in the folder of the package
2. Create/edit the path to the mesh files in the world file
3. Edit the paths in the bringup.launch and the gazebo.launch
4. In the bringup.launch set the coordinates of the place - this is needed by the Qgroundcontrol


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





