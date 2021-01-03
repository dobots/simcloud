# Simcloud
This repository contains packages and setup files to run ROS-based robot simulations. The simulation environment is set up and run using the provided docker image (that needs to be built before use).

## List of environments/worlds
* playground world
* collapsed house world
* fire station world
* coolsingel world
* world with simple shapes (simple_shapes)

## List of robots
* rover - 1 or multiple
* uav - 1 or multiple

## Building the docker image:
If you are new to docker, have a look at the `README_docker.md` file in the `simcloud/docker` folder to install docker and build the image.

## Setup the Simcloud environment

1. Move to the simcloud repository folder:
	```
	cd simcloud
	```

2. Start your docker container from here using the provided script (If it doesn't work you might need to build this docker image):
	```
	./docker/ros_melodic_desktop_px4/run.sh
	```
	**Note:** To open another terminal inside the docker container, run:
	```
	docker exec -it ros_melodic_desktop_px4 /bin/bash
	```
	(Remember to source the scripts below to set up required environment variables in this new terminal as well)

3. Move into the projects folder to access the simcloud files from your host:
	```
	cd /projects/
	```

4. Move into the ros_packages folder (this will be your ros workspace):
	```
	cd ros_packages
	```

5. Run `catkin_make`

6. Source the ROS environment: `source devel/setup.bash`

7. (Optional) If you would like to work with drones, you need to setup the px4 autopilot software. To do this, source the `init_uav_px4.sh` script in the `uav` ROS package (to setup the correct variables):
	```
	source src/uav/scripts/init_uav_px4.sh
	```
	**Note:** If you source your ROS workspace's `setup.bash` file again, you need to re-source the `init_uav_px4.sh` script to setup the ROS_PACKAGE_PATH environment variable. Otherwise the `setup.bash` will overwrite the ROS_PACKAGE_PATH and your program will not find the px4 package.


### Start the environment:
* world with simple shapes:
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

* collapsed fire station
	```
	roslaunch fire_station_description fire_station_world.launch
	```


### Spawn and move robots in an environment:

* Spawn a rover (TODO: add parameters to spawn multiple robots):
	```
	roslaunch rover_gazebo spawn_rover.launch
	```

	Tele-operate the rover using the [IJKL,] keys:
	```
	rosrun teleop_twist_keyboard teleop_twist_keyboard.py
	```

* Spawn a UAV (TODO: add parameters to spawn multiple robots):
	```
	roslaunch uav spawn_uav.launch
	``` 
	You can command the UAV (position control) using the scripts in `pos_control`. For example, run:
	```
	rosrun collapsed_house_pos_control FLYinCollapsedHouse.py
	```
	Finally, you need to arm the drone for flying by running the corresponding mavros commands:
	```
	rosrun mavros mavsys mode -c OFFBOARD
	rosrun mavros mavsafety arm
	```


### (TODO) Spawn robots in an environment using preconfigured launch files:

1. Rover in the shapes environment:

2. Rover in the playground:

3. Rover in the collapsed house:

4. Rover on the Coolsingel:

5. UAV on the Coolsingel:

6. Multiple UAVs and a rover in the collapsed house:






## TODO:
 - ~~move drone pos control to a separate package~~
 - update scripts pointing to the position control package
 - mavros flyscript error?
 - ~~rename mascor_uav package~~
 - ~~rename rover_robot~~
 - ~~correct the dependencies of launch files with the new names~~
 - create instructions in the Readme
 - create videos
 - ~~clean-up the docker image~~
 - add instructions about building the docker image
 - add instructions on how to setup the workspace, etc.
 - add instructions for using QGroundControl


## Future TODO 
    - create new combined launch files for different scenarios
    - use parameters to launch as many robots you want
    - connect to a config file to set parameters

  


## Cheatsheet to use docker
If you have already installed docker then you can use the following lines to start docker and open new terminals. If you need to install it, please jump to the installation section.
1. Move into the folder of the files you would like to use inside docker: 
	```
	cd ~/<path-to-your-ros-packages>/
	```
2. Start docker:
	```
	./<path-to-your-docker-image/run.sh 
	```
3. Inside the docker image move into the `/projects` folder to access the files from your host folder.
	
4. Open a new terminal inside the docker environment:

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


