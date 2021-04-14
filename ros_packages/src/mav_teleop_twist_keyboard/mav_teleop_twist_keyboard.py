#!/usr/bin/env python

from __future__ import print_function

import threading

import roslib; roslib.load_manifest('mav_teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import TwistStamped

from mavros_msgs.srv import CommandBool, SetMode, CommandTOL

import sys, select, termios, tty

msg = """
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


1 : arm and offboard
2: land

r/v : increase/decrease max speeds by 10%
t/b : increase/decrease only linear speed by 10%
y/n : increase/decrease only angular speed by 10%



CTRL-C to quit
"""

moveBindings = {
        'w':(0,0,1,0), # up
        'x':(0,0,-1,0), # down
        'd':(0,0,0,-1), # yaw right (facing)
        'a':(0,0,0,1), # yaw left (facing)
        's':(0,0,0,0), # keep howering
        
        'q':(0,0,1,1), # up and yaw left
        'e':(0,0,1,-1), # up and yaw right
        'z':(0,0,-1,1), # down and yaw left
        'y':(0,0,-1,1), # down and yaw left
        'c':(0,0,-1,-1), # down and yaw right
        
        'i':(0,1,0,0), # pitch forward (slide forward)
        ',':(0,-1,0,0), # pitch backward (slide backward)
        'j':(-1,0,0,0), # roll left (slide left)
        'l':(1,0,0,0), # roll right  (slide right)
        'k':(0,0,0,0), # keep howering

        
        'u':(-1,1,0,0), # pitch forward and roll left
        'o':(1,1,0,0), # pitch forward and roll right
        'm':(-1,-1,0,0), # pitch backward and roll left
        '.':(1,-1,0,0), # pitch backward and roll right
        
    }

speedBindings={
        'r':(1.1,1.1),
        'v':(.9,.9),
        't':(1.1,1),
        'b':(.9,1),
        'y':(1,1.1),
        'n':(1,.9),
    }

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size = 1)
        
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def run(self):
        twistStamped = TwistStamped()
        while not self.done:
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twistStamped.twist.linear.x = self.x * self.speed
            twistStamped.twist.linear.y = self.y * self.speed
            twistStamped.twist.linear.z = self.z * self.speed
            twistStamped.twist.angular.x = 0
            twistStamped.twist.angular.y = 0
            twistStamped.twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twistStamped)

        # Publish stop message when thread exits.
        twistStamped.twist.linear.x = 0
        twistStamped.twist.linear.y = 0
        twistStamped.twist.linear.z = 0
        twistStamped.twist.angular.x = 0
        twistStamped.twist.angular.y = 0
        twistStamped.twist.angular.z = 0
        self.publisher.publish(twistStamped)


def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)




# mavros set mode  -------------------------------------

def setArm():
   rospy.wait_for_service('/mavros/cmd/arming')
   try:
       armService = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
       armService(True)
   except rospy.ServiceException, e:
       print("Service arm call failed: %s"%e)

def setOffboard():
   rospy.wait_for_service('/mavros/set_mode')
   try:
       offboardService = rospy.ServiceProxy('/mavros/set_mode', SetMode)
       offboardService(base_mode=0,custom_mode="OFFBOARD")
   except rospy.ServiceException, e:
       print("Service arm call failed: %s"%e)

       
def setLandMode():
   rospy.wait_for_service('/mavros/cmd/land')
   try:
       landService = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
       isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
   except rospy.ServiceException, e:
       print("service land call failed: %s. The vehicle cannot land "%e)








if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('uav_teleop_twist_keyboard')
    
    
    speed = rospy.get_param("~speed", 0.5)
    turn = rospy.get_param("~turn", 1.0)
    repeat = rospy.get_param("~repeat_rate", 10.0)
    
    key_timeout = rospy.get_param("~key_timeout", 0.0)
    
    if key_timeout == 0.0:
        key_timeout = None

    pub_thread = PublishThread(repeat)
    
    
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(x, y, z, th, speed, turn)
       
        print(msg)
        print(vels(speed,turn))
        #r = rospy.Rate(10)
        while(1):
            key = getKey(key_timeout) 
            
            
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]

                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            elif key == '1':
                print('arm and offboard')
                setArm()
                setOffboard()

            elif key == '2':
                print('land')
                setLandMode()
               
                    
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break
 
            pub_thread.update(x, y, z, th, speed, turn)
           
            
            

    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
