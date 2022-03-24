#!/usr/bin/env python
# -*- coding: latin-1 -*-
 
import rospy
import thread
import threading
from time import time
import mavros
import tf
import math
 
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64

##########################
##########################

pubPosition = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10) 

##########################
##########################

def main():
    rospy.init_node('FLYtoPOS')
    mavros.set_namespace()  # initialize mavros module with default namespace
    rate = rospy.Rate(25)
    rospy.loginfo("Starting...")

    position_msg = PoseStamped()
    position_msg.header.frame_id = "home"

    x = 2
    y = 1
    z = 5


    a = 20
    delta = math.pi/a
    circle_points = list()
    for i in range(0, 2*a):
        px = math.cos(i*delta) + x
        py = math.sin(i*delta) + y
        circle_points.append([px, py])
    
    counter=0
    
    while not rospy.is_shutdown():
	
        
        
        position_msg.header.stamp = rospy.Time.now()
        position_msg.pose.position.x = circle_points[counter][0]
        position_msg.pose.position.y = circle_points[counter][1]
        position_msg.pose.position.z = z

        pubPosition.publish(position_msg)
        print(position_msg.pose.position.x)
        counter += 1
        if counter == 20:
            counter = 0
        rate.sleep()
    
    rospy.loginfo("Bye!")

##########################
##########################

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
