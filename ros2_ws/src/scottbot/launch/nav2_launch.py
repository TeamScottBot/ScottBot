"""
(inside Docker container):
    ros2 launch scottbot nav2_launch.py
    ros2 launch scottbot nav2_launch.py map:=/ScottBot/maps/my_house7.yaml

send a goal:
    ros2 run scottbot delivery_node --ros-args -p target:=living_room
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('scottbot')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    serial_port = LaunchConfiguration('serial_port', default='/dev/ttyUSB0')
    serial_baudrate = LaunchConfiguration('serial_baudrate', default='115200')
    use_rviz = LaunchConfiguration('use_rviz', default='false')

    default_map = '/ScottBot/maps/my_house7.yaml'
    default_params = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(pkg_dir, 'rviz', 'nav2.rviz')

    rplidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        output='screen',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': serial_port,
            'serial_baudrate': serial_baudrate,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
        }],
    )

    base_to_laser_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_to_laser_tf',
        arguments=['0.088', '0.0762', '0.4', '0', '0', '0',
                   'base_footprint', 'laser'],
    )

    odom_node = Node(
        package='scottbot',
        executable='odom_node',
        name='odom_node',
        output='screen',
        parameters=[{
            'linear_scale': 0.1,
            'angular_scale': 0.07,
        }],
    )

    motor_controller_node = Node(
        package='scottbot',
        executable='motor_controller_node',
        name='motor_controller_node',
        output='screen',
    )

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': 'false',
            'autostart': 'true',
        }.items(),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument('map', default_value=default_map,
                              description='Full path to the map yaml'),
        DeclareLaunchArgument('params_file', default_value=default_params,
                              description='Nav2 params yaml'),
        DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('serial_baudrate', default_value='115200'),
        DeclareLaunchArgument('use_rviz', default_value='false'),
        rplidar_node,
        base_to_laser_tf,
        odom_node,
        motor_controller_node,
        nav2_bringup,
        rviz_node,
    ])
