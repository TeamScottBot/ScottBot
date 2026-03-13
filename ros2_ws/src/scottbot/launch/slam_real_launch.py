
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    serial_port = LaunchConfiguration('serial_port', default='/dev/ttyUSB0')
    serial_baudrate = LaunchConfiguration('serial_baudrate', default='115200')
    lidar_frame = LaunchConfiguration('lidar_frame', default='laser')
    linear_scale = LaunchConfiguration('linear_scale', default='0.1')
    angular_scale = LaunchConfiguration('angular_scale', default='0.07')

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
            'linear_scale': linear_scale,
            'angular_scale': angular_scale,
        }],
    )

    motor_controller_node = Node(
        package='scottbot',
        executable='motor_controller_node',
        name='motor_controller_node',
        output='screen',
    )

    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[{
            'use_sim_time': False,
            'solver_plugin': 'solver_plugins::CeresSolver',
            'ceres_linear_solver': 'SPARSE_NORMAL_CHOLESKY',
            'ceres_preconditioner': 'SCHUR_JACOBI',
            'ceres_trust_strategy': 'LEVENBERG_MARQUARDT',
            'ceres_dogleg_type': 'TRADITIONAL_DOGLEG',
            'ceres_loss_function': 'None',
            'correlation_search_space_dimension': 0.5,
            'correlation_search_space_resolution': 0.01,
            'correlation_search_space_smear_deviation': 0.03,
            'loop_search_space_dimension': 8.0,
            'loop_search_space_resolution': 0.05,
            'loop_search_space_smear_deviation': 0.03,
            'loop_search_maximum_distance': 3.0,
            'minimum_travel_distance': 0.1,
            'minimum_travel_heading': 0.15,
            'scan_buffer_size': 10,
            'scan_buffer_maximum_scan_distance': 8.0,
            'use_scan_matching': True,
            'use_scan_barycenter': True,
            'minimum_time_interval': 0.5,
            'resolution': 0.05,
            'minimum_laser_range': 0.12,
            'max_laser_range': 8.0,
            'map_update_interval': 1.0,
            'transform_timeout': 0.2,
            'tf_buffer_duration': 30.0,
            'stack_size_to_use': 40000000,
            'mode': 'mapping',
            'map_file_name': '',
            'map_start_at_dock': True,
            'odom_frame': 'odom',
            'map_frame': 'map',
            'base_frame': 'base_footprint',
            'scan_topic': '/scan',
            'throttle_scans': 2,
            'transform_publish_period': 0.02,
        }],
    )

    return LaunchDescription([
        DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('serial_baudrate', default_value='115200'),
        DeclareLaunchArgument('lidar_frame', default_value='laser'),
        DeclareLaunchArgument('linear_scale', default_value='0.2',
                              description='cmd_vel to real m/s ratio'),
        DeclareLaunchArgument('angular_scale', default_value='0.15',
                              description='cmd_vel to real rad/s ratio'),
        rplidar_node,
        base_to_laser_tf,
        odom_node,
        motor_controller_node,
        slam_toolbox,
    ])
