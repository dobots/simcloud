# mav_teleop_twist_keyboard
Generic keyboard teleop for mavs (micro-aerial-vehicles) based on the teleop twist keyboard package.

# Launch
Run.
```
rosrun mav_teleop_twist_keyboard mav_teleop_twist_keyboard.py _repeat_rate:=10.0
```

With custom values.
```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py _speed:=0.9 _turn:=0.8
```

Publishing to a different topic (in this case `my_cmd_vel`).
```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=my_cmd_vel
```

# Usage
```
Reading from the keyboard  and Publishing to TwistStamped!

---------------------------
Throttle up/down (move up/down) and yaw left/right (rotate left/right):

   q    w    e
   a    s    d
   z    x    c

---------------------------
Pitch up/down(move forward/backward) roll left/right (slide left/right):

   u    i    o
   j    k    l
   m    ,    .


anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
```

# Repeat Rate

MAVs require  constant  updates on the /mavros/setpoint\_velocity/cmd\_vel topic, based on teleop\_twist\_keyboard mav\_teleop\_twist\_keyboard can be configured as well to repeat the last command at a fixed interval, using the `repeat_rate` private parameter.

For example, to repeat the last command at 10Hz:

```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py _repeat_rate:=10.0
```

It is _highly_ recommened that the repeat rate be used in conjunction with the key timeout, to prevent runaway robots.

# Key Timeout

Teleop\_twist\_keyboard can be configured to stop your robot if it does not receive any key presses in a configured time period, using the `key_timeout` private parameter.

For example, to stop your robot if a keypress has not been received in 0.6 seconds:
```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py _key_timeout:=0.6
```

It is recommended that you set `key_timeout` higher than the initial key repeat delay on your system (This delay is 0.5 seconds by default on Ubuntu, but can be adjusted).


### Special thanks to the creators of teleop_twist_keyboard package. This package and Readme is based on the teleop_twist_keyboard package, with slight adjustments to suit controlling mavs.
