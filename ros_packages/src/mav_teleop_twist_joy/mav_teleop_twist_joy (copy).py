#!/usr/bin/env python

# Node to convert /joy messages to /cmd_vel
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import TwistStamped

rospy.init_node('mav_teleop_twist_joy', anonymous=True, disable_signals=True)
rate = rospy.Rate(10) # 10 Hz

# Get axes and scaling from parameter server
l_indx = rospy.get_param('axis_linear', 1)
a_indx = rospy.get_param('axis_angular', 0)
l_scale = rospy.get_param('scale_linear', 1)
print("Linear scaling: ", l_scale)
a_scale = rospy.get_param('scale_angular', 1)
print("Angular scaling: ", a_scale)

def joyCallback(joymsg):
    move.twist.linear.x = l_scale*joymsg.axes[l_indx]
    move.twist.angular.z = a_scale*joymsg.axes[a_indx]
    
# Subscribe to joy topic
rospy.Subscriber('joy', Joy, joyCallback, queue_size=1)

# Publisher to cmd_vel
move = TwistStamped()
pub_cmd_vel = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=1)

while not rospy.is_shutdown():
    pub_cmd_vel.publish(move)
    rate.sleep()
