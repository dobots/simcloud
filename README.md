# Simcloud
This repository contains packages and setup files to run ROS-based robot simulations. The simulation environment is set up and run using the provided docker image (that needs to be built before use).

### List of environments/worlds:

| Empty world | Simple shapes world | Fire station world  |
| ------------- |:-------------:| -----:|
|   <img src="https://github.com/dobots/simcloud/blob/master/images/empty.png" width = "200"/>  | <img src="https://github.com/dobots/simcloud/blob/master/images/simple_shapes.png" width = "200"/> | <img src="https://github.com/dobots/simcloud/blob/master/images/fire_station.png" width = "200"/>|
| **Coolsingel world**      | **Playground world** | **Collapsed house** |
|<img src="https://github.com/dobots/simcloud/blob/master/images/coolsingel.png" width = "200"/> | <img src="https://github.com/dobots/simcloud/blob/master/images/playground.jpg" width = "200"/> | <img src="https://github.com/dobots/simcloud/blob/master/images/collapsed_house.png" width = "200"/>|


### List of robots:
 |Rover | UAV | 
| ------------- |:-------------:| 
|<img src="https://github.com/dobots/simcloud/blob/master/images/rover.png" width = "200"/>|<img src="https://github.com/dobots/simcloud/blob/master/images/uav.png" width = "200"/>|


## Building the docker image:
If you are new to docker, have a look at the `DOCKER_README.md` file in the `simcloud/docker` folder to install docker and see how to build images.

To build the main simcloud image, run the following command from within the directory with the Dockerfile (`simcloud/docker/ros_melodic_desktop_px4/`):
```bash
docker build -t ros_melodic_desktop_px4 .
```

## Running a demo drone simulation:
To run a demonstration of the simulation environment (drone in a fire station), follow the provided `DEMO_README.md` file in the `demo` directory.

## Setting up the Simcloud environment:

1. Move to the simcloud repository folder:
	```bash
	cd simcloud
	```

2. Start your docker container from here using the provided script (If it doesn't work you might need to build this docker image):
	```bash
	./docker/ros_melodic_desktop_px4/run.sh
	```
	**Note:** You can open multiple terminals running in the same docker container. To do this, from the host terminal run:
	```bash
	docker exec -it ros_melodic_desktop_px4 /bin/bash
	```
	(Remember to source the scripts below to set up required environment variables in this new terminal as well)

3. Move into the projects folder to access the simcloud files from your host:
	```bash
	cd /projects/
	```

4. Move into the ros_packages folder (this will be your ros workspace):
	```bash
	cd ros_packages
	```

5. Run `catkin_make`

6. Source the ROS environment: `source devel/setup.bash`

7. (Optional) If you would like to work with drones, you need to setup the px4 autopilot software. To do this, source the `init_uav_px4.sh` script in the `uav` ROS package (to setup the correct variables):
	```bash
	source $(rospack find uav)/scripts/init_uav_px4.sh
	# OR source src/uav/scripts/init_uav_px4.sh
	```
	**Note:** If you source your ROS workspace's `setup.bash` file again, you need to re-source the `init_uav_px4.sh` script to setup the ROS_PACKAGE_PATH environment variable. Otherwise the `setup.bash` will overwrite the ROS_PACKAGE_PATH and your program will not find the px4 package.

### Start the environment:
* world with simple shapes:
	```bash
	roslaunch simple_shapes_description simple_shapes_world.launch
	```

* playground world:
	```bash
	roslaunch playground_world playground_world.launch
	```

* collapsed house world:
	```bash
	roslaunch collapsed_house_description collapsed_house_world.launch
	```

* coolsingel world:
	```bash
	roslaunch coolsingel_description coolsingel_world.launch
	```

* collapsed fire station
	```bash
	roslaunch fire_station_description fire_station_world.launch
	```


### Spawn and move robots in an environment:

* Spawn a rover (TODO: add parameters to spawn multiple robots):
	```bash
	roslaunch rover_gazebo spawn_rover.launch
	```

	Tele-operate the rover using the [IJKL,] keys:
	```bash
	rosrun teleop_twist_keyboard teleop_twist_keyboard.py
	```

* Spawn a UAV (TODO: add parameters to spawn multiple robots):
	```bash
	roslaunch uav spawn_uav.launch
	``` 
	You can command the UAV (position control) using the scripts in `pos_control`. For example, in a new terminal, run:
	```bash
	rosrun collapsed_house_pos_control FLYinCollapsedHouse.py
	```
	Finally, you need to arm the drone for flying by running the corresponding mavros commands in another terminal:
	```bash
	rosrun mavros mavsys mode -c OFFBOARD
	rosrun mavros mavsafety arm
	# OR run `rosrun uav arm_uav.sh`
	```

### Use QGroundControl 

To start QGroundControl move its folder and start the run script:
```
cd /QGroundControl
./qgroundcontrol-start.sh
```
In QGroundControl you can arm and takeoff with the UAV or easily create a mission plan. Try creating a mission plan and see how does it follows the points in Gazebo.

### (TODO) Spawn robots in an environment using preconfigured launch files:

1. Rover in the shapes environment:

2. Rover in the playground:

3. Rover in the collapsed house:

4. Rover on the Coolsingel:

5. UAV on the Coolsingel:

6. Multiple UAVs and a rover in the collapsed house:



## Future TODO:
    - create videos
    - add instructions for using QGroundControl
    - create new combined launch files for different scenarios
    - use parameters to launch as many robots you want
    - connect to a config file to set parameters
    - create cloud hosting


## Cheatsheet to use docker:
If you have already installed docker then you can use the following lines to start docker and open new terminals. If you need to install it, please jump to the installation section.
1. Move into the folder of the files you would like to use inside docker: 
	```bash
	cd ~/<path-to-your-ros-packages>/
	```
2. Start docker:
	```bash
	./<path-to-your-docker-image/run.sh 
	```
3. Inside the docker image move into the `/projects` folder to access the files from your host folder.
	
4. Open a new terminal inside the docker environment:

	```bash
	docker exec -it <name-of-your-docker-image> /bin/bash
	```

5. Source the environment variables in this terminal as well:

	```bash
	. ros_entrypoint.sh
	```
	
7. Move into the projects folder to access files from your host:
	```bash
	cd projects/
	```

8. Move into the ros_packages folder ( this will be your ros workspace):
	```bash
	cd ros_packages
	```

9. Source the environment: `source devel/setup.bash`

### Special thanks to the MASCOR Institute, FH Aachen University of Applied Sciences for their summer school and uav workshop! We have learned a lot from it and it provided an excellent base for creating this repository! 
