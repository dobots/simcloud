# Run a demo drone simulation (fire station):

1. Build the docker image as instructed in **README.md**
	```bash
	cd simcloud/docker/ros_melodic_desktop_px4/
	docker build -t ros_melodic_desktop_px4 .
	```
2. Go to the root simcloud repository folder
	```bash
	cd simcloud
	```
3. Start your docker container from here using the provided script:
	```bash
	./docker/ros_melodic_desktop_px4/run.sh
	# Non-nvidia users can try `run_no_nvidia.sh`
	```
4. At the bash prompt within the container, run:
	```bash
 	./projects/demo/demo_setup.sh
 	# this will build ros_packages, start the gazebo simulation and start RViz
	```
6. From a second terminal prompt in the host machine, run:
	```
	docker exec -it ros_melodic_desktop_px4 bash
	```
7. At the (new) bash prompt within the container, start: 
	```bash
	./projects/demo/launch_pos_control.sh
	```
8. From a third terminal prompt, run:
	```
	docker exec -it ros_melodic_desktop_px4 bash
	```
9. At this new bash prompt within the container, start: 
	```bash
	./projects/demo/launch_uav.sh
	```
10. In the Gazebo screen you'll see the drone starting to fly around and inside the collapsed building.