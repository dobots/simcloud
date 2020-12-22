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
###### Functions #########
##########################

def rectangle_circumference(cx = 0, cy = 0, w = 10, h = 5):
    rectangle_points = list()
    rectangle_points.append([cx - w/2, cy + h/2])
    rectangle_points.append([cx + w/2, cy + h/2])
    rectangle_points.append([cx + w/2, cy - h/2])
    rectangle_points.append([cx - w/2, cy - h/2])

    return rectangle_points
    


def callback(msg):
    current_pos_x = msg.pose.position.x
    current_pos_y = msg.pose.position.y
    current_pos_z = msg.pose.position.z

    global target_points
    global target_position_x
    global target_position_y
    global counter
    if math.sqrt((target_position_x-current_pos_x)**2 + (target_position_y-current_pos_y)**2) < 3.0:
        counter = counter + 1
        if counter == len(target_points): counter = 0
        target_position_x = target_points[counter][0]
        target_position_y = target_points[counter][1]


##########################


pubPosition = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)
subscriber = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback)        
counter = -1

##call rectangle_circumference
target_points = rectangle_circumference()
target_position_x = target_points[0][0]
target_position_y = target_points[0][1]
    

def main():
    
    rospy.init_node('FLYtoPOS')
    mavros.set_namespace()  # initialize mavros module with default namespace
    rate = rospy.Rate(25)
    rospy.loginfo("Starting...")
    print("Starting...")

    position_msg = PoseStamped()
    position_msg.header.frame_id = "home"
    
    

    global target_position_x
    global target_position_y


    while not rospy.is_shutdown():

        position_msg.header.stamp = rospy.Time.now()

        position_msg.pose.position.x = target_position_x
        position_msg.pose.position.y = target_position_y
        position_msg.pose.position.z = 8

        pubPosition.publish(position_msg)
        print(position_msg)
        rate.sleep()
    
    rospy.loginfo("Bye!")

##########################
##########################

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
