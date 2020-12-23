# DockerPathfinder

This Docker image provides a fully integrated ROS Melodic, Gazebo, PixHawk simulator setup.


## Usage

1. Download this repository
2. Go into the folder with the Dockerfile.
3. To build the image, run: *docker build -t ros_melodic_desktop_px4 .*
   (This takes a really long time! And uses ~7.5GB of space)
4. You can start the image through: *./run.sh*
   (If you start this script from a catkin workspace folder, this workspace will be available in */projects* within the container)

## Running the full firestation demo

1. Follow steps 1-3 above
2. Download https://github.com/dobots/drones (private, contact us if you need access)
3. Go into the drones project folder
4. Start */`<fullPath2DockerPathFinder>`/run_rosgazebo.sh*
5. At the bash prompt within the container, start: *./demo_setup.sh* (this will pop-up gazebo and RViz)
6. From a second terminal prompt, run: *docker exec -it gazebo_test bash*
7. At the (new) bash prompt within the container, start: *launch_demo_script.sh*
8. From a third terminal prompt, run: *docker exec -it gazebo_test bash*
9. At this new bash prompt within the container, start: *launch_demo.sh*
10. In the Gazebo screen you'll see the drone starting to fly around the collapsed building




