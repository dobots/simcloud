# rover_cart_description
The **urdf** is main folder of the package. It describes the rover cart for a gazebo simulation. 

## urdf
This folder describes the rover cart, with a base and two front wheels and two casters, on top of the base an artag is added. 

**base_rover_cart.urdf.xacro**: connects all the urdf files. The main `base_link` has an inertia, collision and visual block. The inertia block needs to be compared with the real life rover cart. The visual block links to the mesh of the rover cart. The wheel, caster and artag are added as a xacro.

**base_rover_cart.gazebo.xacro**: defines the plugin for gazebo and some specific values for the controller can be set. 

**wheel.urdf.xacro**: describes the front wheel of the cart. The position and friction need to be double checked. The wheel rotate the wrong direction when operated with the `cmd_vel/` topic. 

**caster.urdf.xacro**: creates a simple friction free collision block on the place of the caster wheel. 

**artag.urdf.xacro**: adds an artag to the cart. The size of the artag is 0.5m x 0.5m which makes it easily visible for the drone. It is possible to change the texture to a different kind of marker, the number can easily be change. 

**caster.urdf.xacro**: creates a simple friction free collision block on the place of the caster wheel. 

**artag.urdf.xacro**: adds an artag to the cart. The size of the artag is 0.5m x 0.5m which makes it easily visible for the drone. It is possible to change the texture to a different kind of marker, the number can easily be changed in the `base_rover_cart.urdf.xacro`.

## meshes
Holds the meshes for the `base_rover_cart.urdf` and `wheel.urdf`. The blender folder can be used to cut or orientate the meshes differently. 

## header & source files
These contain a set up for a tf broadcaster node. 

## media
The material for the artag is defined here. 

## gzweb
In order for the model to work with gzweb a .SDF of the rover was generated.
1) use `rosrun xacro xacro` to generate a .URDF file
2) use `gz sdp -p filename.urdf > filename.sdf` to generate a .SDF file
3) set the model.config to use the sdf file

Surface textures/logos seem to break the sdf conversion, thus they should be uncommented beforehand 
