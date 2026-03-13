#    ros2 launch scottbot drive_to_goal_launch.py


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    serial_port = LaunchConfiguration('serial_port', default='/dev/ttyUSB0')

    # map : 169x222, res=0.05, origin=[-4.77,-4.81]
    #   start  ≈ world (0, 0)     → grid (125, 95)
    #   goal ≈ world (-0.5, 3.5) → grid (55, 85)
    start_cell = LaunchConfiguration('start', default='[140, 140]')
    goal_cell = LaunchConfiguration('goal', default='[105, 78]')
    map_file = LaunchConfiguration('map_file',
                                   default='/ScottBot/maps/my_house7.yaml')

    rplidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        output='screen',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': serial_port,
            'serial_baudrate': 115200,
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

    astar_planner = Node(
        package='scottbot',
        executable='astar_planner',
        name='astar_planner_node',
        output='screen',
        parameters=[{
            'map_file': map_file,
            'start': start_cell,
            'goal': goal_cell,
            'robot_radius_cells': 2,
            'initial_heading_deg': 90.0,
        }],
    )

    nav_executor = Node(
        package='scottbot',
        executable='nav_executor',
        name='nav_executor_node',
        output='screen',
        parameters=[{
            'linear_speed': 0.15,
            'angular_speed': 0.4,
            'cmd_linear': 0.3,
            'cmd_angular': 0.5,
            'pause_between': 0.5,
        }],
    )

    return LaunchDescription([
        DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('map_file',
                              default_value='/ScottBot/maps/my_house7.yaml'),
        DeclareLaunchArgument('start', default_value='[140, 140]'),
        DeclareLaunchArgument('goal', default_value='[105, 78]'),
        rplidar_node,
        base_to_laser_tf,
        odom_node,
        motor_controller_node,
        astar_planner,
        nav_executor,
    ])
