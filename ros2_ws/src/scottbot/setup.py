from setuptools import setup
import os
from glob import glob

package_name = 'scottbot'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ScottBot Team',
    maintainer_email='scottbot@ucr.edu',
    description='ScottBot: UCR food delivery robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_node = scottbot.camera_node:main',
            'obstacle_detector_node = scottbot.obstacle_detector_node:main',
            'motor_controller_node = scottbot.motor_controller_node:main',
            'lidar_node = scottbot.lidar_node:main',
        ],
    },
)
