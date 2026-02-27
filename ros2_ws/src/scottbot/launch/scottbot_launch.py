"""Launch file – starts all ScottBot nodes together."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='scottbot',
            executable='camera_node',
            name='camera_node',
            output='screen',
        ),
        Node(
            package='scottbot',
            executable='obstacle_detector_node',
            name='obstacle_detector_node',
            output='screen',
        ),
        Node(
            package='scottbot',
            executable='motor_controller_node',
            name='motor_controller_node',
            output='screen',
        ),
        Node(
            package='scottbot',
            executable='lidar_node',
            name='lidar_node',
            output='screen',
        ),
    ])
