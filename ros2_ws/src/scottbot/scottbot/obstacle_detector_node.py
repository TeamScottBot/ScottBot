"""Obstacle detector node – subscribes to camera images and publishes a Bool on /blocked."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Bool


class ObstacleDetectorNode(Node):
    """Processes camera frames to detect obstacles and publishes to /blocked."""

    def __init__(self):
        super().__init__('obstacle_detector_node')
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
        self.publisher_ = self.create_publisher(Bool, '/blocked', 10)
        self.get_logger().info('ObstacleDetectorNode started')

    def image_callback(self, msg: Image):
        # TODO: run obstacle detection on the incoming image
        # For now, always publish False (no obstacle)
        blocked_msg = Bool()
        blocked_msg.data = False
        self.publisher_.publish(blocked_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
