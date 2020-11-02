#  How to get started with Docker images

## Step 1: Install Docker
Install Docker: [https://docs.docker.com/engine/install/ubuntu/](https://meet.google.com/linkredirect?authuser=1&dest=https%3A%2F%2Fdocs.docker.com%2Fengine%2Finstall%2Fubuntu%2F)
To run docker without super user:
```
  sudo groupadd docker
  sudo gpasswd -a ${USER} docker
  sudo service docker restart
```

> **_NOTE:_** To check whether you can run Docker without sudo or just to test the installation run: 
	    `docker run hello-world` or to check your Docker version:`docker  -v`

## Step 2: Install Nvidia acceleration:
[https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker](https://meet.google.com/linkredirect?authuser=1&dest=https%3A%2F%2Fdocs.nvidia.com%2Fdatacenter%2Fcloud-native%2Fcontainer-toolkit%2Finstall-guide.html%23docker)


## Step 3: Build the Docker containers

Move into the folder of the docker image you would like to use and build it:
	```
	cd ~/docker
	cd ros2_focal
	docker build -t ros2_focal .	
	```
	> **_NOTE:_** Check if your image has been succesfully build: `docker image list`

## Step 4: Start the container
	
```
cd ros2_focal
./run.sh
```
Try to run e.g.: `ros2 run turtlesim turtlesim_node`
	
> **_NOTE:_**  In case of errors make the script executable and try to run it again: `chmod +x run.sh`


## Step 5: Using multiple terminals
To open a new terminal window run:
```
docker exec -it ros2_focal /bin/bash
# Source the environment variables
. ros_entrypoint.sh
```
Run e.g teleop in the new terminal:`ros2 run turtlesim turtle_teleop_key`

## Step 6: Creating a ROS workspace, which is connected to the filesystem outside of the Docker container

Move in to the directory where you would like to create your ROS workspace:`cd`
Then run the Docker container from this folder:
```
\your\path\to\the\docker\container\run.sh
```
Inside the Docker container move into the `projects` directory. Everything what you do inside the projects directory will be stored in the folder where you started your Docker image. e.g.
```
cd projects
mkdir -p simcloud_ws/src
cd simcloud_ws/
catkin_make
```

 
 
