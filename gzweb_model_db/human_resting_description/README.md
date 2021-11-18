# Human resting description

Contains the 3D model of a human figure lying on the ground.

To use this 3D model in your environment, include the following code in your .world file:


    <model name="human">
        <static>true</static>
       <pose>5.4 3.5 0.8 0 3.14 -1.57</pose>
        <link name="body"> 
       <visual name="visual">
            <geometry>
              <mesh>
                <uri>model://human_resting_description/gazebo_model/meshes/man_resting.dae</uri>
              </mesh>
            </geometry>
            <cast_shadows>true</cast_shadows>
          </visual>
      <collision name="collision">
           <geometry>
              <mesh>
                <uri>model://human_resting_description/gazebo_model/meshes/man_resting.dae</uri>
              </mesh>
            </geometry>
          </collision>
        </link>
      </model>

