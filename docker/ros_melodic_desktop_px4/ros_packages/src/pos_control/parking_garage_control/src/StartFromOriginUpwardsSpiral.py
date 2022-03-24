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
    
    # ground level 
    path_points.append([-5, -5, 3]) #2
    path_points.append([-10, -10, 3]) #3
    path_points.append([-26.3, -11.2, 3]) #5
    path_points.append([-39.6, -11.3, 3]) #6
    path_points.append([-38.6, 0, 3]) #12
    # first floor 
    path_points.append([-35, 0, 3.2]) #2
    path_points.append([-32, 0, 3.6]) #2
    path_points.append([-24, 0, 5]) #2
    path_points.append([-16.8, -1.3, 7]) #3
    path_points.append([-17.1, -11.1, 7]) #4
    path_points.append([-26.3, -11.2, 7]) #5
    path_points.append([-39.6, -11.3, 7]) #6
    path_points.append([-39.0, 12, 7]) #7
    path_points.append([-24.3, 10.5, 7]) #human subject
    path_points.append([-20.2, 13.6, 7]) #9
    path_points.append([-19.5, 23.3, 7]) #10
    path_points.append([-40.0, 20.9, 7]) #11
    path_points.append([-38.6, 0.2, 7]) #12
    
    # second  floor 
    path_points.append([-30, 0, 8]) #2
    path_points.append([-26, 0, 11]) #2
    path_points.append([-16.8, -1.3, 13.1]) #3
    path_points.append([-17.1, -11.1, 13.1]) #4
    path_points.append([-26.3, -11.2, 13.1]) #5
    path_points.append([-39.6, -11.3, 13.1]) #6
    path_points.append([-39.0, 12, 13.1]) #7
    path_points.append([-24.3, 10.5, 13.1]) #human subject
    path_points.append([-20.2, 13.6, 13.1]) #9
    path_points.append([-19.5, 23.3, 13.1]) #10
    path_points.append([-40.0, 20.9, 13.1]) #11
    path_points.append([-38.6, 0.2, 13.1]) #12
    
    # third floor
    path_points.append([-30, 0, 14]) #2
    path_points.append([-25, 0, 16]) #2
    path_points.append([-16.8, -1.3, 19.0]) #3 level
    path_points.append([-17.1, -11.1, 19.0]) #4
    path_points.append([-26.3, -11.2, 19.0]) #5
    path_points.append([-39.6, -11.3, 19.0]) #6
    path_points.append([-39.0, 12, 19.0]) #7
    path_points.append([-24.3, 10.5, 19.0]) #human subject
    path_points.append([-20.2, 13.6, 19.0]) #9
    path_points.append([-19.5, 23.3, 19.0]) #10
    path_points.append([-40.0, 20.9, 19.0]) #11
    path_points.append([-38.6, 0.2, 19.0]) #12
# 
    #path_points.append([11, 3.6, 7.1]) #5
    #path_points.append([11, 3.6, 3.2]) #4
    #path_points.append([7.2, 1.4, 2.8]) #2
    #path_points.append([0, 1.4, 2.8]) #1

  

    return path_points
    


def callback(msg):
    current_pos_x = msg.pose.position.x
    current_pos_y = msg.pose.position.y
    current_pos_z = msg.pose.position.z

    global target_points
    global target_position_x
    global target_position_y
    global target_position_z

    global counter
    if math.sqrt((target_position_x-current_pos_x)**2 + (target_position_y-current_pos_y)**2 + (target_position_z-current_pos_z)**2) < 1.0:
        counter = counter + 1
        if counter == len(target_points): counter = 0
        target_position_x = target_points[counter][0]
        target_position_y = target_points[counter][1]
        target_position_z = target_points[counter][2]


##########################


pubPosition = rospy.Publisher('/move_base_simple/goal',PoseStamped, queue_size=10)
subscriber = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback)        
counter = -1

##call rectangle_circumference
target_points = path_list()
target_position_x = target_points[0][0]
target_position_y = target_points[0][1]
target_position_z = target_points[0][2]
    

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
    global target_position_z


    while not rospy.is_shutdown():

        position_msg.header.stamp = rospy.Time.now()

        position_msg.pose.position.x = target_position_x
        position_msg.pose.position.y = target_position_y
        position_msg.pose.position.z = target_position_z

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
