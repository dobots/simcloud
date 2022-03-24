# mav_teleop_twist_joy
PS joystick teleop for mavs (micro-aerial-vehicles) based on the teleop twist keyboard package.

# Launch
Set the ros paramater to your joystick:
```
rosparam set joy_node/dev "/dev/input/jsX"
```

Start the ros joy_node:
```
rosrun joy joy_node
```

Run.
```
rosrun mav_teleop_twist_joy mav_teleop_twist_joy.py
```

With custom values.
```
rosrun teleop_twist_joy teleop_twist_joy.py _speed:=0.9 _turn:=0.8
```

Publishing to a different topic (in this case `my_cmd_vel`).
```
rosrun teleop_twist_joy teleop_twist_joy.py cmd_vel:=my_cmd_vel
```


# Usage
```
Reading from a joystick  and Publishing to TwistStamped!

---------------------------
Left stick: Throttle up/down (move up/down) and yaw left/right (rotate left/right):


          Throttle up  
                   
  Yaw left    o      Yaw right
         
         Throttle down    


---------------------------
Right stick: Pitch up/down(move forward/backward) roll left/right (slide left/right):

         Pitch forward  
                   
 Roll left    o     Roll right
         
        Pitch backward  


--------------------------
action button circle : arm and offboard
action button cross : land


action buttons triangle/square : increase/decrease max speeds by 10%
directional buttons up/down : increase/decrease only linear speed by 10%
directional buttons left/right : increase/decrease only angular speed by 10%

CTRL-C to quit
```

# Repeat Rate

MAVs require  constant  updates on the /mavros/setpoint\_velocity/cmd\_vel topic, based on teleop\_twist\_keyboard mav\_teleop\_twist\_joy can be configured as well to repeat the last command at a fixed interval, using the `repeat_rate` private parameter. The default repeat rate is 10Hz.

For example, to repeat the last command at 20Hz:

```
rosrun teleop_twist_joy teleop_twist_joy.py _repeat_rate:=20.0
```

It is _highly_ recommened that the repeat rate be used in conjunction with the key timeout, to prevent runaway robots.

# Key Timeout

Teleop\_twist\_joy can be configured to stop your robot if it does not receive any key presses in a configured time period, using the `key_timeout` private parameter.

For example, to stop your robot if a keypress has not been received in 0.6 seconds:
```
rosrun teleop_twist_joy teleop_twist_joy.py _key_timeout:=0.6
```

It is recommended that you set `key_timeout` higher than the initial key repeat delay on your system (This delay is 0.5 seconds by default on Ubuntu, but can be adjusted).


### Special thanks to the creators of teleop_twist_keyboard package. This package and Readme is based on the teleop_twist_keyboard package, with slight adjustments to suit controlling mavs.  The code snippet used to set the mode of the uav to offboard, arm, and land was copied from https://edu.gaitech.hk/gapter/mavros-basics.html Special thanks to the authors of those tutorials as well!
