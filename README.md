# ScottBot
## Overview
ScottBot is an automated food delivery solution for UCR, allowing students and faculty to order food without needing to interrupt their work or walk across campus.

## Repo Contents
[**``/api``**](/api/): Contains all of our api endpoints and cloudflare configuration files. For more details see the readme in this folder.

[**``/frontend``**](/frontend/): Contains the source files for our frontend. For more details see the readme in this folder

[**``/pi``**](/pi/): Contains testing files to ensure the Raspberry Pi can connect and use the other parts of the robot properly. This includes connecting to the websocket, using data from the LiDAR, and using the motors to avoid obstacles.

[**``/ros2ws``**](/ros2_ws/): Contains our Ros2 workspace, which we use to map and navigate the environment. Commands for running the pathfinding and other scripts are at the top of relevant files.

[**``/rplidar_docker``**](/rplidar_docker/): Contains the main docker file for running commands and scripts on the robot.

[**``/maps``**](/maps/): Contains lidar generated maps of our testing environment
