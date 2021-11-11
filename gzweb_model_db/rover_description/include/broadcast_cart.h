/*
 * Author: bart 
 * Date: 25/09/2019
 *
 This is the header file of the start_search node.
 */

#ifndef broadcast_cart_H
#define broadcast_cart_H

// include all necessary files, functions, and messages
#include <ros/ros.h>
#include <gazebo_msgs/ModelState.h>
#include <gazebo_msgs/GetModelState.h>
#include <ros/service.h>
#include <tf/transform_broadcaster.h>
//#include <geometry_msgs/PoseStamped.h>

// The class definition is inside the talker namespace. Namespaces are used. e collisions.
namespace transform_cart{

	// Class definition
	class Transform{
	  	public:
    // constructor definition
	    Transform(std::string name);
	// member functions
		void callbc();
		tf::TransformBroadcaster br;
		
		private:
	// attributes
		ros::NodeHandle nh_; 
		ros::ServiceClient cart_pos_cl_; // service for arming
		gazebo_msgs::GetModelState modelstate_;
		std::string name_;	
		tf::Transform transform;
		//tf::Quaternion q;

	}; // end class
} // end namespace

#endif 
