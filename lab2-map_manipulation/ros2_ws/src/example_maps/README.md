# example_maps
Example ROS maps

Example use with map server: 

$ ros2 run nav2_map_server map_server --ros-args --params-file src/example_maps/param/map_server_params.yaml

$ ros2 lifecycle set /map_server configure

$ ros2 lifecycle set /map_server activate

Turtlebot + OctoMap:

ros2 launch example_maps turtlesim3_waffle_octomap.launch
