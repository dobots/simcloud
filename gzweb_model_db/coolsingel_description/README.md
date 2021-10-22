# Coolsingel description
Contains the 3D model of the Coolsingel. In addition it contains launch files to start the gazebo environment with a UAV. 

ROS package, which includes the mesh files, sdf description, world description and a launch file to launch  a world with the Coolsingel

**1. Run the launch file:**

    roslaunch coolsingel_description coolsingel_world.launch
	
or include the following code snippet in your launch file:

    <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="$(find coolsingel_description)/worlds/coolsingel_world.world"/>
    </include>
	
**2. Then the UAV can fly on a given path using QGroundControl mission function.**



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

## Converting 3D models from OpenStreetMap to .stl format

 1.   Select the region of interest in Open Street Map and Export it
		 - Go to the website  [Open Street Map](http://www.openstreetmap.org/).
   
	  - Click the  **Export**  button at the top of the screen.

	  - Fill in the latitude and longitude coordinate range (scroll through the coordinate fields by pressing a  **Tab**  key to view an area on the map).
	  -  Click the  **Export**  button the left side of the screen (the file extension will be  _.osm_).

 2. Map editing
	- Visit the site  _https://josm.openstreetmap.de/wiki/Download_  to download the  JOSM  application  _josm-tested.jar_.

	- Open an application with the command: 

	 	 `java -jar josm-tested.jar`

	- Choose the  _.osm_  extension file.

	- Changes to map attributes are made in the right part of the application.

	- Save the changes

3. 3D Map Creation

	- Access the website  _http://osm2world.org/_  to download the  [OSM2world](http://osm2world.org/)  application.

	- Open an application with the command:

	    `java -jar OSM2World.jar`

	- Check out the changes performed in the previous step.

	- Export the file to the object format (_.obj_).

4. Conversion from  _.obj_  format to  _.stl_  format.
	- Documentation:  _http://www.openscenegraph.org/index.php/documentation/guides/user-guides/55-osgconv_

	- Run the command:
	
		`osgconv map_pucrs.obj map_pucrs.stl`


[Converting 3D models from OpenStreetMap to .stl format copied from: https://pucrs-campus-on-gazebo.readthedocs.io/en/latest/source/campus/](https://pucrs-campus-on-gazebo.readthedocs.io/en/latest/source/campus/)


