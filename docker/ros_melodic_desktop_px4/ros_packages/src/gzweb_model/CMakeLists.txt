cmake_minimum_required(VERSION 2.8.3)
project(gzweb_model)

find_package(catkin REQUIRED)

catkin_package()

install(PROGRAMS gzweb_model.bash DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
