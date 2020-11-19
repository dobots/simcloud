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

def path_list():
    path_points = list()
    path_points.append([0, -0.5]) #1
    #path_points.append([4.7, -0.5]) #2
    #path_points.append([4.7, -3.5]) #3
    path_points.append([4.9, -2.7]) #rover position
    path_points.append([5.2, -2.7]) #door opening
    path_points.append([6.5, -3.5]) #4
    path_points.append([8.8, -0.5]) #5
    path_points.append([8.8, 2]) #6
    path_points.append([8.8, 4]) #7
    path_points.append([11, 4]) #8
    path_points.append([11, 2]) #9
    path_points.append([8.8, 2]) #10
    path_points.append([8.8, -0.5]) #11
    path_points.append([5.5, -0.5]) #12
    path_points.append([5.5, 2]) #13
    path_points.append([5.5, 4]) #14
    path_points.append([4.7, 4]) #15
    path_points.append([4.7, 2]) #16

    #Go back
    path_points.append([5.8, 2]) #13
    path_points.append([5.8, -0.5]) #12
    path_points.append([6.5, -3.5]) #4
    path_points.append([5.2, -2.7]) #door opening
    path_points.append([4.9, -2.7]) #rover position
    #path_points.append([4.7, -3.5]) #3
    #path_points.append([4.7, -0.5]) #2
    path_points.append([0, -0.5]) #1
    
    

    return path_points
    


def callback(msg):
    current_pos_x = msg.pose.position.x
    current_pos_y = msg.pose.position.y
    current_pos_z = msg.pose.position.z

    global target_points
    global target_position_x
    global target_position_y
    global counter
    if math.sqrt((target_position_x-current_pos_x)**2 + (target_position_y-current_pos_y)**2) < 0.4:
        counter = counter + 1
        if counter == len(target_points): counter = 0
        target_position_x = target_points[counter][0]
        target_position_y = target_points[counter][1]


##########################


pubPosition = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)
subscriber = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback)        
counter = -1

##call rectangle_circumference
target_points = path_list()
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
        position_msg.pose.position.z = 1.4

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
