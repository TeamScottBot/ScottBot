"""Camera node – publishes raw images from the Raspberry Pi Camera Module 3."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class CameraNode(Node):
    """Captures frames from the Pi camera and publishes to /camera/image_raw."""

    def __init__(self):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('CameraNode started')

    def timer_callback(self):
        # TODO: capture frame from Pi camera (picamera2 or cv2.VideoCapture)
        # and publish as sensor_msgs/Image
        pass


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
