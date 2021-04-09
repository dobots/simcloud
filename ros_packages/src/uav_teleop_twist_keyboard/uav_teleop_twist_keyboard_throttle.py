#!/usr/bin/env python

# import #
import rospy
from geometry_msgs.msg import TwistStamped

# node initialization #
rospy.init_node("uav_teleop_throttle")

# definitions of variables #
msg_cmd_vel = TwistStamped()

# definitions of functions #
def callback(msg_teleop):
    global msg_cmd_vel
    msg_cmd_vel = msg_teleop



# definition of publisher/subscriber and services #
pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=1)
rospy.Subscriber('/teleop_uav/cmd_vel', TwistStamped, callback)

# main program #
r = rospy.Rate(20) #5 Hz

while not rospy.is_shutdown():

    # write a string to the ROS message field
    pub.publish(msg_cmd_vel)
    r.sleep()



