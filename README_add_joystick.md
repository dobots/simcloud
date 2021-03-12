# Setup Dualshock 3 controller for flying a PX4 based UAV in Gazebo

## 1. USB cable connection

### 1.1. Connect the PS3 joystick to your computer with an USB cable and press Ps button to connect it.
### 1. 2. Check if Linux recognized your joystick:  

* You should  see a listing of all of your input devices similar to below by typing `ls /dev/input/`:

```
by-id    event0  event2  event4  event6  event8  mouse0  mouse2  uinput
by-path  event1  event3  event5  event7  js0     mice    mouse1
```

As you can see above, the joystick devices are referred to by jsX ; in this case, our joystick is js0. Let's make sure that the joystick is working.
```
sudo jstest /dev/input/jsX
```
You will see the output of the joystick on the screen. Move the joystick around to see the data change.

```
Driver version is 2.1.0.
Joystick (Logitech Logitech Cordless RumblePad 2) has 6 axes (X, Y, Z, Rz, Hat0X, Hat0Y)
and 12 buttons (BtnX, BtnY, BtnZ, BtnTL, BtnTR, BtnTL2, BtnTR2, BtnSelect, BtnStart, BtnMode, BtnThumbL, BtnThumbR).
Testing ... (interrupt to exit)
Axes:  0:     0  1:     0  2:     0  3:     0  4:     0  5:     0 Buttons:  0:off  1:off  2:off  3:off  4:off  5:off  6:off  7:off  8:off  9:off 10:off 11:off
```


### 1.3. Access the joystick from inside the container

**Short explanation of possible solutions followed by a solution for a joystick**
Accessing devices from inside a docker container is a bit tricky.
The most common suggestion is to use the  `--privileged`  flag while starting a docker container. But from a security perspective, that is a terrible thing to do. Using the  `--privileged`  flag would give the container access and all capabilities to all the devices connected to the host (i.e. everything under the  `/dev`  directory).

**Using the --device flag**
The  `--device`  exposes devices to a container. This method works fine. But it gives you access only to the devices that were connected to the host while starting the continer. If you reconnect a device, or connect a new device, then you won't be able to access it from inside the container.

**Using the --device-cgroup-rule flag**

The  `--device-cgroup-rule`  flag allows you add a more permissive rule to a container allowing it access to a wider range of devices. In a way, this flag also allows you to limit access only to some devices.

Before creating the container, you need to know the major and minor number of the device you want the container to have access to. You can find the major and minor number of a device by running the  `ls -l`  command on your device or device directory.
Here the major number is  `189`. And the number after  `189`  is the minor number for the corresponding device.  

```
ls -l /dev/bus/usb/001/
total 0
crw-rw-r--  1 root root  189, 0 Dec 13 18:09 001
crw-rw-r--  1 root root  189, 1 Dec 13 18:09 002
crw-rw-r--  1 root root  189, 2 Dec 13 18:09 003
crw-rw-r--  1 root root  189, 3 Dec 13 18:09 004
crw-rw-r--  1 root root  189, 4 Dec 13 18:09 005
crw-rw-r--  1 root root  189, 5 Dec 13 18:09 006
crw-rw----+ 1 root audio 189, 6 Dec 13 19:48 007

```
The  `device-cgroup-rule`  is written in the following format:  
```
type major:minor mode

type: a (all), or b (block), or c (char)
major and minor: either a number, or * for all
mode: a composition of r (read), w (write), and m (mknod)
```

Now start a container with the  `--device-cgroup-rule`  flag. This gives the container access to all the devices with major number  `189`.  
```
sudo docker run \
--rm -it \
--device /dev/bus/usb \
--device-cgroup-rule 'a 189:* rwm' \
ubuntu:20.04

ls /dev
```
If you want the container to have access to all the devices, you could use  `--device-cgroup-rule 'a *:* rwm'`.

So everything should work fine now, right? Not really. If you try to reconnecting a device, or connect a new device, you still won't be able to access it from inside the container. You need to run the  `mknod`  command inside the container each time there is a device change. That's too much work. There is a better way to solve this problem.

**Mounting the devices as a volume**
Instead of using the  `--device`  flag, mount the devices or device directory as a volume.  
```
sudo docker run \
--rm -it \
-v /dev/bus/usb:/dev/bus/usb \
--device-cgroup-rule 'a 189:* rwm' \
ubuntu:20.04

ls /dev
```
Now it would work perfectly fine with both old and new devices, as long as the device has a major number  `189`.

Source:
https://dev.to/jeetparekh/accessing-devices-from-inside-a-docker-container-without-using-the-privileged-flag-1dd8

**Solution for a joystick**
```
ls /dev/input/
```
The output fill be similar to:
```
crw-rw-r--  1 root root  189, 0 Dec 13 18:09 001
crw-rw-r--  1 root root  189, 1 Dec 13 18:09 002
```
The next thing you need to do is edit the run.sh file, by adding the following lines:
```
...
docker run -iPt \
...
    -v /dev/bus/usb:/dev/bus/usb \
    -v /dev/input:/dev/input \
...
    ros_melodic_desktop_px4 \
    bash
```

### 1.4. Make it accessible for the ROS joy node.**
Start your docker container:
```
./docker/ros_melodic_desktop_px4/run.sh
```
To test whether you can read the joystick data inside the container run:
```
sudo jstest /dev/input/jsX
```
You migh need to install jstest:
```
sudo apt-get install -y jstest-gtk
```

Start by listing the permissions of the joystick:
```
ls -l /dev/input/jsX
```
You will see something similar to:
```
crw-rw-XX- 1 root dialout 188, 0 2009-08-14 12:04 /dev/input/jsX
```
If XX is rw: the js device is configured properly.
If XX is --: the js device is not configured properly and you need to:
```
$ sudo chmod a+rw /dev/input/jsX
```
**Starting the Joy Node**
To get the joystick data published over ROS we need to start the joy node. First let's tell the joy node which joystick device to use- the default is js0. You might need to change it to js1. (**Don't forget the / before the dev: "/dev/input/js1"**)

```
$ roscore
$ rosparam set joy_node/dev "/dev/input/jsX"
```
Now we can start the joy node.
```
$ rosrun joy joy_node
```
You will see something similar to:
```
[ INFO] 1253226189.805503000: Started node [/joy], pid [4672], bound on [aqy], xmlrpc port [33367], tcpros port [58776], logging to [/u/mwise/ros/ros/log/joy_4672.log], using [real] time

[ INFO] 1253226189.812270000: Joystick device: /dev/input/js0

[ INFO] 1253226189.812370000: Joystick deadzone: 2000
```
Now in a '''new terminal''' you can `rostopic echo` the joy topic to see the data from the joystick:

```
$ rostopic echo joy
```
As you move the joystick around, you will see something similar to :
```
---
axes: (0.0, 0.0, 0.0, 0.0)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, 0.0, 0.12372203916311264)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, -0.18555253744125366, 0.12372203916311264)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, -0.18555253744125366, 0.34022033214569092)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, -0.36082032322883606, 0.34022033214569092)
buttons: (0, 0, 0, 0, 0)
```


Source:
http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick

### 1.5. Run teleop with a rover

Start a launch file with a rover and then run:
```
rosrun joy joy_node
rosrun teleop_twist_joy teleop_node
```
Hold down the X button on the controller and control the rover with the left joystick. Don't forget to keep the teleop_twist_joy window active to be able to control the rover.

### 1.6. Run teleop with Qgroundcontrol on a UAV

https://docs.qgroundcontrol.com/master/en/SetupView/Joystick.html



## 2. Bluetooth based connection - TODO

Start your systems bluetooth:
https://www.linux.org/threads/ubuntu-20-04-64-bits-how-install-ps3-controller-driver-and-remove-qtsixa.32355/

Instructions on how to pair your controller:
https://askubuntu.com/questions/913599/how-to-connect-dualshock-3-controller-ps3-sixaxis-gamepad-on-ubuntu-16-04


Error:
```
checking for BLUEZ... no
configure: error: Package requirements (bluez >= 5.0) were not met:

No package 'bluez' found

Consider adjusting the PKG_CONFIG_PATH environment variable if you
installed software in a non-standard prefix.

Alternatively, you may set the environment variables BLUEZ_CFLAGS
and BLUEZ_LIBS to avoid the need to call pkg-config.
See the pkg-config man page for more details.
```

After quiet a long search we found out that  
`sudo apt-get install libbluetooth-dev` was the package that was missing. Mentioning this in the dependencies list would be great

## Access device from inside the container
https://dev.to/jeetparekh/accessing-devices-from-inside-a-docker-container-without-using-the-privileged-flag-1dd8

Before startign the container kill the bluetooth deivces:
sudo killall -9 bluetoothd
Otherwise, you will get a D-Bus error

Install jstest:
https://zoomadmin.com/HowToInstall/UbuntuPackage/jstest-gtk

https://forum.openmediavault.org/index.php?thread/33649-how-to-get-a-bluetooth-device-in-a-container/

https://community.home-assistant.io/t/bluetooth-in-docker/46547

https://www.reddit.com/r/homeassistant/comments/j5g4v2/i_got_bt_working_in_docker_only_took_hours/

https://medium.com/george-adams-iv/using-raspberry-pi-3-s-bluetooth-in-docker-e9cdf6062d6a

https://github.com/moby/moby/issues/16208

https://community.home-assistant.io/t/bluetooth-in-docker/46547

https://forums.balena.io/t/bluetooth-within-docker-compose/3460

https://ubuntuforums.org/archive/index.php/t-1190061-p-5.html



