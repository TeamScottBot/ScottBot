"""SLAM launch file – runs slam_toolbox alongside the simulation."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command


def generate_launch_description():
    pkg_dir = get_package_share_directory('scottbot')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'sim_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'world': os.path.join(pkg_dir, 'worlds', 'obstacles.world'),
            'rviz': 'false',  # we launch our own RViz with map display
        }.items(),
    )

    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            # Solver
            'solver_plugin': 'solver_plugins::CeresSolver',
            'ceres_linear_solver': 'SPARSE_NORMAL_CHOLESKY',
            'ceres_preconditioner': 'SCHUR_JACOBI',
            'ceres_trust_strategy': 'LEVENBERG_MARQUARDT',
            'ceres_dogleg_type': 'TRADITIONAL_DOGLEG',
            'ceres_loss_function': 'None',
            # Matcher
            'correlation_search_space_dimension': 0.5,
            'correlation_search_space_resolution': 0.01,
            'correlation_search_space_smear_deviation': 0.1,
            'loop_search_space_dimension': 8.0,
            'loop_search_space_resolution': 0.05,
            'loop_search_space_smear_deviation': 0.03,
            'loop_search_maximum_distance': 3.0,
            # Scan processing
            'minimum_travel_distance': 0.3,
            'minimum_travel_heading': 0.3,
            'scan_buffer_size': 10,
            'scan_buffer_maximum_scan_distance': 10.0,
            'use_scan_matching': True,
            'use_scan_barycenter': True,
            'minimum_time_interval': 0.5,
            # General
            'resolution': 0.05,
            'max_laser_range': 12.0,
            'map_update_interval': 1.0,
            'transform_timeout': 0.2,
            'tf_buffer_duration': 30.0,
            'stack_size_to_use': 40000000,
            # Map
            'mode': 'mapping',
            'map_file_name': '',
            'map_start_at_dock': True,
            # Frames
            'odom_frame': 'odom',
            'map_frame': 'map',
            'base_frame': 'base_footprint',
            'scan_topic': '/scan',
            # Throttle
            'throttle_scans': 1,
            'transform_publish_period': 0.02,
            'map_update_interval': 1.0,
        }],
    )

    rviz_config = os.path.join(pkg_dir, 'rviz', 'slam.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        sim_launch,
        slam_toolbox,
        rviz_node,
    ])
