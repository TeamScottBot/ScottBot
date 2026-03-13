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

## Necessary Commands 
### Docker Setup
Build Docker image
```jsx
docker build -t my_rplidar_env ./rplidar_docker
```

Run Docker container
```jsx
docker run -it --rm --name rplidar_container --privileged --net=host --device=/dev/ttyUSB1 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v /home/colemiller/ScottBot:/ScottBot my_rplidar_env
```

### Terminal #1

You should be inside the container now. (root@raspberrypi:~/ros2_ws#)

This terminal will be for running SLAM. The SLAM launch file (slam_real_launch.py) starts the official RPLidar ROS2 driver (`sllidar_node`), which publishes LaserScan data to `/scan` for SLAM.

Link package and build:

```jsx
ln -s /ScottBot/ros2_ws/src/scottbot ~/ros2_ws/src/scottbot
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Launch SLAM (THE USB PORT NUMBER MAY BE DIFFERENT):

```jsx
ros2 launch scottbot slam_real_launch.py serial_port:=/dev/ttyUSB1
```

### Terminal #2

IN ANOTHER TERMINAL:

This terminal will be for activating the motor controller.

```jsx
docker exec -it rplidar_container bash
source ~/ros2_ws/install/setup.bash
ros2 run scottbot motor_controller_node
```

### Terminal #3

IN ANOTHER TERMINAL:

This terminal will be for moving the robot.

```jsx
docker exec -it rplidar_container bash
source ~/ros2_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Terminal #4

This terminal will be used to save the map.

```jsx
docker exec -it rplidar_container bash
source ~/ros2_ws/install/setup.bash
ros2 run nav2_map_server map_saver_cli -f /ScottBot/maps/scottbot_map
```
