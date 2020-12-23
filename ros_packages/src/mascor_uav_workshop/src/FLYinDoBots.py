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

def circle_circumference(cx = -5,cy = 0, a = 10):
    circle_points = list()
    delta = math.pi/a   
    for i in range(0, 2*a):
        px = 5*math.cos(i*delta) + cx
        py = 5*math.sin(i*delta) + cy
        circle_points.append([px, py])

    return circle_points
    

def rectangle_circumference(cx = 0, cy = 0, w = 10, h = 10):
    rectangle_points = list()
    rectangle_points.append([cx      , cy      ])
    rectangle_points.append([cx      , cy - h/2 - h/2.5])
    rectangle_points.append([cx      , cy - h/2])
    rectangle_points.append([cx + w  , cy - h/2])
    rectangle_points.append([cx + w  , cy + h/2])
    rectangle_points.append([cx      , cy + h/2])
    rectangle_points.append([cx      , cy      ])

    return rectangle_points
   

def callback(msg):
    current_pos_x = msg.pose.position.x
    current_pos_y = msg.pose.position.y
    current_pos_z = msg.pose.position.z

    global target_points
    global target_position_x
    global target_position_y
    global counter
    if math.sqrt((target_position_x-current_pos_x)**2 + (target_position_y-current_pos_y)**2) < 1.0:
        counter = counter + 1
        if counter == len(target_points): counter = 0
        target_position_x = target_points[counter][0]
        target_position_y = target_points[counter][1]


##########################


pubPosition = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)
subscriber = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback)        
counter = -1

##call circle_circumference
target_points_O = circle_circumference()
target_points_D = rectangle_circumference()
target_points = target_points_D + target_points_O
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