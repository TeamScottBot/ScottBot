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

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    map_yaml = LaunchConfiguration(
        'map',
        default=os.path.join(pkg_dir, 'maps', 'example_apartment.yaml'),
    )
    launch_sim = LaunchConfiguration('sim', default='false')
    launch_rviz = LaunchConfiguration('rviz', default='true')

    # initial 
    initial_x = LaunchConfiguration('initial_x', default='0.0')
    initial_y = LaunchConfiguration('initial_y', default='0.0')
    initial_yaw = LaunchConfiguration('initial_yaw', default='0.0')

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'yaml_filename': map_yaml,
        }],
    )

    # AMCL
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,

            # frames
            'base_frame_id': 'base_footprint',
            'odom_frame_id': 'odom',
            'global_frame_id': 'map',

            'update_min_d': 0.1,
            'update_min_a': 0.2,

            'max_particles': 2000,
            'min_particles': 500,

            'laser_model_type': 'likelihood_field',
            'laser_max_range': 12.0,
            'laser_min_range': 0.15,
            'max_beams': 60,

            'robot_model_type': 'nav2_amcl::OmniMotionModel',
            'alpha1': 0.2,
            'alpha2': 0.2,
            'alpha3': 0.2,
            'alpha4': 0.2,
            'alpha5': 0.1,

            # start pose
            'set_initial_pose': True,
            'initial_pose_x': initial_x,
            'initial_pose_y': initial_y,
            'initial_pose_yaw': initial_yaw,

            'recovery_alpha_slow': 0.001,
            'recovery_alpha_fast': 0.1,

            'tf_broadcast': True,
        }],
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'node_names': ['map_server', 'amcl'],
        }],
    )

    # gazebo
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', 'sim_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'world': os.path.join(pkg_dir, 'worlds', 'obstacles.world'),
            'rviz': 'false',
        }.items(),
        condition=IfCondition(launch_sim),
    )

    # RViz
    rviz_config = os.path.join(pkg_dir, 'rviz', 'nav.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
        condition=IfCondition(launch_rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('map', default_value=os.path.join(
            pkg_dir, 'maps', 'example_apartment.yaml')),
        DeclareLaunchArgument('sim', default_value='false'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('initial_x', default_value='0.0'),
        DeclareLaunchArgument('initial_y', default_value='0.0'),
        DeclareLaunchArgument('initial_yaw', default_value='0.0'),

        sim_launch,
        map_server,
        amcl,
        lifecycle_manager,
        rviz_node,
    ])
