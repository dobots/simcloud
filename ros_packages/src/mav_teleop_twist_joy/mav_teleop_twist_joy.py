#!/usr/bin/env python

from __future__ import print_function

import threading

import roslib; roslib.load_manifest('mav_teleop_twist_joy')
import rospy

from sensor_msgs.msg import Joy
from geometry_msgs.msg import TwistStamped

from mavros_msgs.srv import CommandBool, SetMode

import sys, select, termios, tty

msg = """
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
action button cross : stop


action buttons triangle/square : increase/decrease max speeds by 10%
directional buttons up/down : increase/decrease only linear speed by 10%
directional buttons left/right : increase/decrease only angular speed by 10%

CTRL-C to quit
"""



speedBindings={
        'button[2]' :(1.1,1.1), # triangle
        'button[3]' :(0.9,0.9), # square
        'button[13]':(1.1,1.0), #dir. button up
        'button[14]':(0.9,1.0), #dir. button down
        'button[15]':(1.0,1.1), #dir. button left
        'button[16]':(1.0,0.9), #dir. button right
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




def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

joymsg = None    
def joyCallback(msg):
    global joymsg
    joymsg = msg

        

def getSpeedBindingsKey(buttons, button_ind):
   key = None
   
   if button_ind and buttons[button_ind] == 0: # last active button is released
        key = "button[%d]" % (button_ind) # create a key 
        button_ind = None    # reset the index

   for num, button in enumerate(buttons):  # look for active buttons    
      if button: # if a button is pressed
         button_ind = num # store its id
         break;

                  
   return button_ind, key


def setArm():
   rospy.wait_for_service('/mavros/cmd/arming')
   try:
       armService = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
       armService(True)
   except rospy.ServiceException, e:
       print("Service arm call failed: %s"%e)



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
    
    # Subscribe to joy topic
    rospy.Subscriber('joy', Joy, joyCallback, queue_size=1)
    

        
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0
    button_index = None

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(x, y, z, th, speed, turn)
     
        while(1):
           
            if joymsg is not None:
                x = joymsg.axes[3]
                y = joymsg.axes[4]
                z = joymsg.axes[1]
                th = joymsg.axes[0]
                button_index,key = getSpeedBindingsKey(joymsg.buttons, button_index)
                                
                if key in speedBindings.keys(): # directional buttons change speed
                    speed = speed * speedBindings[key][0]
                    turn = turn * speedBindings[key][1] 
                    print(vels(speed,turn))                
                
                             
                if key == 'button[1]': #action button circle : arm and offboard
                    print('arm and offboard')
                    setArm()         
                
                
            
                #action button cross : stop
                #if joymsg.buttons[0]: #cross
                #   KeyboardInterrupt               
                
                
                
               
            pub_thread.update(x, y, z, th, speed, turn)
        
           
            
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
    
    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)     
