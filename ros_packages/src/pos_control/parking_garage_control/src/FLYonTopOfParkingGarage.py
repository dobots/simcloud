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
    # path_points.append([-10, 0.4, 3]) #1
    # path_points.append([-10, 31, 8]) #2
    # path_points.append([-32, 31, 9.75]) #2.5
    # path_points.append([-52, 31, 11.5]) #3
    # path_points.append([-52, -31, 15]) #4
    # path_points.append([-32, -31, 16.75]) #4.5
    # path_points.append([-10, -31, 18.5]) #5
    # path_points.append([-10, 0, 22]) #6
    # path_points.append([-10, 31, 25.5]) #2
    # path_points.append([-32, 31, 27]) #2.5
    # path_points.append([-52, 31, 29]) #3
    # path_points.append([-52, -31, 32.5]) #4
    # path_points.append([-32, -31, 34]) #4.5
    # path_points.append([-10, -31, 36]) #5
    path_points.append([-10, 0, 20]) #
    path_points.append([-10, 0, 42.5]) #

    # Enter building from top
    path_points.append([-22, 0, 42.5])
    path_points.append([-30, 0, 36.5])
    path_points.append([-36, 0, 35.5])

    # Circle around Top
    # path_points.append([-12, 21, 46]) #2
    # path_points.append([-28, 21, 46]) #2.5
    # path_points.append([-35, 21, 46]) #3
    # path_points.append([-35, -21, 46]) #4
    # path_points.append([-28, -21, 46]) #4.5
    # path_points.append([-12, -21, 46]) #5
    # path_points.append([-12, 0, 46]) #6
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
    if math.sqrt((target_position_x-current_pos_x)**2 + (target_position_y-current_pos_y)**2 + (target_position_z-current_pos_z)**2) < 2:
        counter = counter + 1
        if counter == len(target_points): counter = 0
        target_position_x = target_points[counter][0]
        target_position_y = target_points[counter][1]
        target_position_z = target_points[counter][2]


##########################


pubPosition = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
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
    
    x_offset = 0.35
    y_offset = 0.4
    z_offset = 0.275

    global target_position_x
    global target_position_y
    global target_position_z


    while not rospy.is_shutdown():

        position_msg.header.stamp = rospy.Time.now()

        position_msg.pose.position.x = target_position_x - x_offset
        position_msg.pose.position.y = target_position_y - y_offset
        position_msg.pose.position.z = target_position_z - z_offset

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
