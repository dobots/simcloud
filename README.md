# Simcloud

## List of environments
* world with simple shapes 
* playground world
* collapsed house world
* fire station world 
* coolsingel world


## List of robots
* rover - 1 or multiple
* uav - 1 or multiple


# Setup the Simcloud environment

1. Move into the simcloud folder:
```
cd ~/simcloud
```

4. Start your docker environment from here (If it doesn't work you might need to build this docker image):
```
~/docker/ros_melodic_desktop_full/run.sh
```

5. Open a new terminal inside the Docker environment:
```
docker exec -it ros_melodic_desktop_full /bin/bash
```

6. Source the environment variables in this terminal as well:
```
. ros_entrypoint.sh
```
7. Move into the projects folder to access files from your host:
```
cd projects/
```

8. (Optional) If you would like to work with drones run the init_drone.sh script to setup the correct variables:
```
. init_drone.sh
```
Important to have a space between the . and the init_drone.sh command, otherwise it'll not setup the correct path variables , because of the `#!/bin/bash` command at the top of the script.


8. Move into the ros_packages folder ( this will be your ros workspace):
```
cd ros_packages
```

8. Run `catkin_make`

9. Source the environment: `source devel/local_setup.bash` If you source the setup.bash file instead of the local version and you are working with drones, you need to run the init_drone.sh script to reconfigure the ROS_PACKAGE_PATH. Otherwise your program will not find mavros, mavlink, and px4.


## Start the environment:
* world with simple shapes - create for the workshop one blender mesh:
```
roslaunch simple_shapes_description simple_shapes_world.launch
```



* playground world:

```
roslaunch playground_world playground_world.launch
```

* collapsed house world:
```
roslaunch collapsed_house_description collapsed_house_world.launch
```


* coolsingel world:
```
roslaunch coolsingel_description coolsingel_world.launch
```



## Spawn robots in an empty environment:

Spawn a rover (to do add parameters to spawn at a given location or spawn multiple):

```
roslaunch rover_gazebo spawn_rover.launch
```

Spawn a UAV (to do add parameters to spawn at a given location or spawn multiple):




## Spawn robots in an environment using preconfigured launch files:

1. Rover in the shapes environment:

2. Rover in the playground:

3. Rover in the collapsed house:

4. Rover on the Coolsingel:

5. UAV on the Coolsingel:

6. Multiple UAVs and a rover in the collapsed house:






## TODO:
 - ~~move drone pos control to a separate package~~
 - update scripts pointing to the position control package
 - rename mascor_uav package
 - ~~rename rover_robot~~
 - ~~correct the dependencies of launch files with the new names~~
 - create instructions in the Readme
 - create videos
 - ~~clean-up the docker image~~
 - add instructions about building the docker image
 - add instructions on how to setup the workspace, etc.


## Future TODO 
    - create new combined launch files for different scenarios
    - use parameters to launch as many robots you want
    - connect to a config file to set parameters

  


## Cheatsheet to use Docker
If you have already installed Docker then you can use the following lines to start Docker and open new terminals. If you need to install it, please jump to the installation section.
1. Move into the folder of the files you would like to use inside Docker: 
	```
	cd ~/<path-to-your-ros-packages>/
	```
2. Start Docker:
	```
	./<path-to-your-docker-image/run.sh 
	```
3. Inside the Docker image move into the `/projects` folder to access the files from your host folder.
	
4. Open a new terminal inside the Docker environment:

	```
	docker exec -it <name-of-your-docker-image> /bin/bash
	```

5. Source the environment variables in this terminal as well:

	```
	. ros_entrypoint.sh
	```
	
7. Move into the projects folder to access files from your host:
```
cd projects/
```

8. Move into the ros_packages folder ( this will be your ros workspace):
```
cd ros_packages
```

9. Source the environment: `source devel/setup.bash`


