/*
 * Author: bart
 * Date: 17/10/2019
This is source code of the artag_follow node. 
 */

// All declarations of variables and functions are described in the header.
#include <broadcast_cart.h>

// The class definition is inside its namespace.
namespace transform_cart{
	// Constructs instance of the class
	Transform::Transform(std::string name){ 
		name_ = name;
		// get model position
		cart_pos_cl_ = nh_.serviceClient<gazebo_msgs::GetModelState>("gazebo/get_model_state", "{model_name = rover}"); 
		//Transform::callbc();
	};
	
	void Transform::callbc(){	
		//wait for service
		cart_pos_cl_.waitForExistence();
		if (cart_pos_cl_.call(modelstate_))	
        	ROS_INFO("position received");
		else
            ROS_ERROR("Failed to call service get_model_state of rover");
			
		// define the tranform
		std::cout << "received x position ="<< modelstate_.response.pose.position.x << std::endl;	
		std::cout << "received y position ="<< modelstate_.response.pose.position.y << std::endl;
		std::cout << "received z position ="<< modelstate_.response.pose.position.z << std::endl;
		std::cout << "received orientation ="<< modelstate_.response.pose.orientation << std::endl;

		transform.setOrigin(tf::Vector3( modelstate_.response.pose.position.x, 
										 modelstate_.response.pose.position.y,
 										 modelstate_.response.pose.position.z));
		//q = modelstate_.pose.orientation;
		//transform.setRotation();

 		br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "map", "base_footprint"));
		ros::Duration(2).sleep();
	}
} // end namespace
