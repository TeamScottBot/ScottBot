"""LIDAR node – publishes LaserScan data from the LIDAR sensor."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarNode(Node):
    """Reads from the LIDAR sensor and publishes to /scan."""

    def __init__(self):
        super().__init__('lidar_node')
        self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('LidarNode started')

    def timer_callback(self):
        # TODO: read from LIDAR hardware (e.g. rplidar SDK)
        # and publish as sensor_msgs/LaserScan
        pass


def main(args=None):
    rclpy.init(args=args)
    node = LidarNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
