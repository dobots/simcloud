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
from ar_track_alvar_msgs.msg import AlvarMarkers
from std_msgs.msg import Float64

import tf2_ros
from geometry_msgs.msg import TransformStamped

import time

time_now = None
time_prev = time.time()
time_to_next_z_change = 10

##########################
##########################



pubPosition = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)

target_position_x = 0
target_position_y = 0
target_position_z = 15


##########################
##########################


def follow_ar():

    global target_position_x
    global target_position_y
    global target_position_z
    global transformData
    target_position_x = transformData.transform.translation.x
    target_position_y = transformData.transform.translation.y


#subscriber = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback)        
#subscriber = rospy.Subscriber("/ar_pose_marker", AlvarMarkers, follow_ar)


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
    global time_to_next_z_change
    global transformData

    transformData = TransformStamped()        #setup object to receive transform
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)   #setup tf listener

    while not rospy.is_shutdown():
        #lookup for the newest transform
        #transformData = tfBuffer.lookup_transform('usb_camera::camera_link', 'ar_marker_13', rospy.Time(0))
        try:
            transformData = tfBuffer.lookup_transform('map', 'ar_marker_13', rospy.Time(0))
            follow_ar()
            print transformData
            print '########'

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            pass
        
        time_now = time.time()
        if (time_now - time_prev) >= time_to_next_z_change:
            time_to_next_z_change = 1
            if position_msg.pose.position.z < 5: target_position_z = target_position_z - 1
            else: target_position_z = target_position_z - 0.2
            if position_msg.pose.position.z < 0.1:
                target_position_z = 0


        position_msg.header.stamp = rospy.Time.now()

        position_msg.pose.position.x = target_position_x
        position_msg.pose.position.y = target_position_y
        position_msg.pose.position.z = target_position_z
        print target_position_x
        print target_position_y
        print target_position_z

        pubPosition.publish(position_msg)
        #print(position_msg)
        rate.sleep()

    rospy.loginfo("Bye!")

##########################
##########################

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
