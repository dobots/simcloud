#!/usr/bin/env python
# -*- coding: latin-1 -*-

#debugging script used for tf transfomration investigation 

import rospy
from time import time
import tf
import math

from sensor_msgs.msg import Imu
from mavros_msgs.msg import Altitude
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from std_msgs.msg import Float64

br = tf.TransformBroadcaster()

altitude = 0
orientation = (0,0,0,1)
orientation_home = (0,0,0,1)
localPosition = (0,0,0)
footprintPosition = (0,0,0)
markerPosition = (0,0,0)
worldPosition = (0,0,0) 

##########################
##########################

def callbackAltitude(msg):
    global altitude
    altitude = msg.local

def callbackImu(msg):
    global orientation, orientation_normalized
    orientation = (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w)
    euler = tf.transformations.euler_from_quaternion(orientation)
    roll = -euler[0]
    pitch = -euler[1]
    yaw = 0
    orientation_normalized = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

def callbackLocalPosition(msg):
    global localPosition, footprintPosition
    localPosition = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
    footprintPosition = [msg.pose.position.x, msg.pose.position.y, 0]


##########################
##########################
  
rospy.Subscriber('/mavros/altitude', Altitude, callbackAltitude)    
rospy.Subscriber('/mavros/imu/data', Imu, callbackImu)   
rospy.Subscriber('/mavros/local_position/pose', PoseStamped, callbackLocalPosition)  


##########################
##########################

def main():
    global worldPosition, localPosition, footprintPosition,  altitude, orientation
    rospy.init_node('FramesPublisher')
    rate = rospy.Rate(25)
    rospy.loginfo("Publishing frames...")
    #CAMERA ORIENTATION
    roll    = math.pi
    pitch   = 0
    yaw     = -(math.pi/2)
    orientation_camera = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

    while not rospy.is_shutdown():

        br.sendTransform(worldPosition,
                         (0, 0, 0, 1), 
                         rospy.Time.now(), 
                         "copter_home", 
                         "world")


        br.sendTransform(localPosition,
                         orientation, 
                         rospy.Time.now(), 
                         "copter_base_link", 
                         "copter_home")

        br.sendTransform(footprintPosition,
                         (0, 0, 0, 1),
                         rospy.Time.now(),
                         "copter_base_footprint",
                         "copter_home")

        br.sendTransform((0, 0, 0),
                         orientation_camera,
                         rospy.Time.now(),
                         "usb_camera::camera_link",
                         "copter_base_link") 
               
        rate.sleep()
    
    rospy.loginfo("Bye!")

##########################
##########################

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
