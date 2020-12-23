/*
 * Author: bart
 * Date: 23/09/2019
 */

// All declarations of variables and functions are described in the header.

#include <broadcast_cart.h>

int main(int argc, char **argv){
  	// Initialize ros
  	ros::init(argc, argv, "broadcast_cart_node");
	ROS_INFO("ros initiated");
	// object made.
  	transform_cart::Transform change("rover");
	ros::Rate rate(20);
	
	while(ros::ok()){
		change.callbc();
		//ROS_INFO("go object made");
		rate.sleep();
		ros::spinOnce();
	}
	return 0;
}
