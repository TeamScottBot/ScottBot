"""Motor controller node – subscribes to /blocked and /cmd_vel to drive the motors."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


class MotorControllerNode(Node):
    """Drives motors based on Nav2 velocity commands, with emergency stop from /blocked."""

    def __init__(self):
        super().__init__('motor_controller_node')

        self.blocked = False

        self.blocked_sub = self.create_subscription(
            Bool, '/blocked', self.blocked_callback, 10
        )
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10
        )
        self.get_logger().info('MotorControllerNode started')

    def blocked_callback(self, msg: Bool):
        self.blocked = msg.data
        if self.blocked:
            self.get_logger().warn('Obstacle detected – stopping motors')
            self._stop_motors()

    def cmd_vel_callback(self, msg: Twist):
        if self.blocked:
            self.get_logger().info('Ignoring cmd_vel – blocked')
            return
        # TODO: translate msg.linear.x and msg.angular.z into motor PWM signals
        self.get_logger().debug(
            f'cmd_vel: linear={msg.linear.x:.2f} angular={msg.angular.z:.2f}'
        )

    def _stop_motors(self):
        # TODO: send zero PWM to motor driver
        pass


def main(args=None):
    rclpy.init(args=args)
    node = MotorControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
