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

8. Move into the ros_packages folder ( this will be your ros workspace):
```
cd ros_packages
```

8. Run `catkin_make`

9. Source the environment: `source devel/setup.bash`

10. Start your launch file e.g. `roslaunch playground_world playground_world.launch`






TODO:
    
2.  start collecting packages and updating the readme
    
3.  take the rover descritpion/ tb3 description
    
4.  show files what is in there
    
5.  create a gazebo folder
    
6.  empty world. launch
    
7.  spawn a rover
    
8.  do it in one file
    
9.  creating environments
    
10.  copy the description folder
    
11.  set the config files
    
12.  create a mesh or use gazebo mesh files in a world file
    
13.  create a mesh file - edit in blender, or download
    
14.  add the mesh file
    
15.  create a launch file in the gazebo folder
    
16.  do it 3 times - 3 environments
    
17.  spawn rover separately at a given location using parameters or use the combined launch files
    

  

18.  copy a drone gazebo folder
    
19.  copy a drone description folder
    
20.  clean both up, remove all the other package dependencies
    
21.  keep only what is necessary and copy here what is needed from other packages
    
22.  spawn a drone separately at a given location using parameters or use the combined launch files
    

  

23.  create a rover and drone folder
    
24.  launch both of them in different environments using combined launch files
    
25.  or use parameters to launch as many you want at a given location
    
26.  add namespace parameter to the rover and location parameters
