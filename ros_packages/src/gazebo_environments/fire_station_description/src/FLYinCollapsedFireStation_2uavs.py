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

def path_list1():
    path_points = list()
    path_points.append([2.9, 1.1, 2.4]) #rover position
    path_points.append([7.0, 1.1, 2.4]) #2
    path_points.append([10.8, -10.1, 2.3]) #3
    path_points.append([11, 2.0, 2.8]) #4

    path_points.append([7.0, 1.1, 2.6]) #2

    return path_points
    

def path_list2():
    path_points = list()
    #1. floor
    path_points.append([2.9, 3, 2.6]) #rover position
    path_points.append([7.0, 3, 2.6]) #2
    path_points.append([11, 4.1, 3.1]) #4
    path_points.append([11, 4.1, 7.1]) #5
    # 2. floor
    path_points.append([12.58, 8.8, 7.1]) #6
    path_points.append([9.24, 9.35, 7.1]) #7
    path_points.append([11, 3.6, 7.1]) #8
    path_points.append([9.5, -1.68, 7.1]) #9
    path_points.append([10.32, -4.7, 7.1]) #10
    path_points.append([7.8, -4.98, 7.1]) #11
    path_points.append([9.5, -1.68, 7.1]) #12
    path_points.append([11, 4.1, 7.1]) #5
    # 1. floor
    path_points.append([11, 4.1, 3.1]) #4
    path_points.append([7.0, 2.5, 2.4]) #2

    return path_points


def callback1(msg):
    current_pos_x = msg.pose.position.x
    current_pos_y = msg.pose.position.y
    current_pos_z = msg.pose.position.z

    global target_points1
    global target_position1_x
    global target_position1_y
    global target_position1_z
    global counter1

    if math.sqrt((target_position1_x-current_pos_x)**2 + (target_position1_y-current_pos_y)**2 + (target_position1_z-current_pos_z)**2) < 0.4:
        counter1 = counter1 + 1
        if counter1 == len(target_points1): counter1 = 0
        target_position1_x = target_points1[counter1][0]
        target_position1_y = target_points1[counter1][1]
        target_position1_z = target_points1[counter1][2]


def callback2(msg):
    current_pos_x = msg.pose.position.x
    current_pos_y = msg.pose.position.y
    current_pos_z = msg.pose.position.z

    global target_points2
    global target_position2_x
    global target_position2_y
    global target_position2_z
    global counter2

    if math.sqrt((target_position2_x-current_pos_x)**2 + (target_position2_y-current_pos_y)**2 + (target_position2_z-current_pos_z)**2 ) < 0.4:
        counter2 = counter2 + 1
        if counter2 == len(target_points2): counter2 = 0
        target_position2_x = target_points2[counter2][0]
        target_position2_y = target_points2[counter2][1]
        target_position2_z = target_points2[counter2][2]

##########################


pubPosition1 = rospy.Publisher('/uav0/mavros/setpoint_position/local', PoseStamped, queue_size=10)
subscriber1 = rospy.Subscriber("/uav0/mavros/local_position/pose", PoseStamped, callback1)  

pubPosition2 = rospy.Publisher('/uav1/mavros/setpoint_position/local', PoseStamped, queue_size=10)
subscriber2 = rospy.Subscriber("/uav1/mavros/local_position/pose", PoseStamped, callback2) 
      
counter1 = -1
counter2 = -1


##call rectangle_circumference
target_points1 = path_list1()
target_position1_x = target_points1[0][0]
target_position1_y = target_points1[0][1]
target_position1_z = target_points1[0][2]


target_points2 = path_list2()
target_position2_x = target_points2[0][0]
target_position2_y = target_points2[0][1]
target_position2_z = target_points2[0][2]    

def main():
    
    rospy.init_node('FLYtoPOS')
    mavros.set_namespace()  # initialize mavros module with default namespace
    rate = rospy.Rate(25)
    rospy.loginfo("Starting...")
    print("Starting...")

    position1_msg = PoseStamped()
    position1_msg.header.frame_id = "home"
    
    position2_msg = PoseStamped()
    position2_msg.header.frame_id = "home"    

    global target_position1_x
    global target_position1_y
    global target_position1_z

    global target_position2_x
    global target_position2_y
    global target_position2_z


    while not rospy.is_shutdown():

        position1_msg.header.stamp = rospy.Time.now()
        position1_msg.pose.position.x = target_position1_x
        position1_msg.pose.position.y = target_position1_y
        position1_msg.pose.position.z = target_position1_z

        pubPosition1.publish(position1_msg)
        print(position1_msg)


        position2_msg.header.stamp = rospy.Time.now()
        position2_msg.pose.position.x = target_position2_x
        position2_msg.pose.position.y = target_position2_y
        position2_msg.pose.position.z = target_position2_z

        pubPosition2.publish(position2_msg)
        print(position2_msg)



        rate.sleep()
    
    rospy.loginfo("Bye!")

##########################
##########################

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
