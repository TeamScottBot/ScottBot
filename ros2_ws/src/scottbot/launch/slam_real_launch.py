"""SLAM launch file for real robot – RPLidar + slam_toolbox (no simulation)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    serial_port = LaunchConfiguration('serial_port', default='/dev/ttyUSB0')
    serial_baudrate = LaunchConfiguration('serial_baudrate', default='115200')  # A1: 115200, A2/A3/S1/S2: 256000
    lidar_frame = LaunchConfiguration('lidar_frame', default='laser')

    rplidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        output='screen',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': serial_port,
            'serial_baudrate': serial_baudrate,
            'frame_id': lidar_frame,
            'inverted': False,
            'angle_compensate': True,
        }],
    )

    # --- Static TF: base_footprint → laser ---
    # Adjust xyz to match where the LIDAR is mounted on your robot
    base_to_laser_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_to_laser_tf',
        arguments=['0.088', '0.0762', '0.4', '0', '0', '0', 'base_footprint', 'laser'],
    )

    # --- Static TF: odom → base_footprint (identity) ---
    # Without wheel encoders, slam_toolbox will handle localization
    # via scan-matching alone. This gives it the required odom frame.
    odom_to_base_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='odom_to_base_tf',
        arguments=['0', '0', '0', '0', '0', '0',
                   'odom', 'base_footprint'],
    )

    # --- slam_toolbox ---
    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[{
            'use_sim_time': False,
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
        }],
    )

    return LaunchDescription([
        DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('serial_baudrate', default_value='115200'),
        DeclareLaunchArgument('lidar_frame', default_value='laser'),
        rplidar_node,
        base_to_laser_tf,
        odom_to_base_tf,
        slam_toolbox,
    ])
