import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped, Quaternion
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster


def yaw_to_quaternion(yaw: float) -> Quaternion:
    q = Quaternion()
    q.z = math.sin(yaw / 2.0)
    q.w = math.cos(yaw / 2.0)
    return q


class OdomNode(Node):

    def __init__(self):
        super().__init__('odom_node')

        self.declare_parameter('linear_scale', 0.1)
        self.declare_parameter('angular_scale', 0.07)

        self.linear_scale = self.get_parameter('linear_scale').value
        self.angular_scale = self.get_parameter('angular_scale').value

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.vx = 0.0
        self.vy = 0.0
        self.vtheta = 0.0

        self.tf_broadcaster = TransformBroadcaster(self)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)

        self.create_subscription(Twist, '/cmd_vel', self._cmd_vel_cb, 10)

        self.dt = 0.02  # 50 Hz
        self.create_timer(self.dt, self._update)

        self.get_logger().info(
            f'OdomNode started (linear_scale={self.linear_scale}, '
            f'angular_scale={self.angular_scale})'
        )

    def _cmd_vel_cb(self, msg: Twist):
        self.vx = msg.linear.x * self.linear_scale
        self.vy = msg.linear.y * self.linear_scale
        self.vtheta = msg.angular.z * self.angular_scale

    def _update(self):
        dx = (self.vx * math.cos(self.theta) - self.vy * math.sin(self.theta)) * self.dt
        dy = (self.vx * math.sin(self.theta) + self.vy * math.cos(self.theta)) * self.dt
        dtheta = self.vtheta * self.dt

        self.x += dx
        self.y += dy
        self.theta += dtheta

        now = self.get_clock().now().to_msg()
        q = yaw_to_quaternion(self.theta)

        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation = q
        self.tf_broadcaster.sendTransform(t)

        odom_msg = Odometry()
        odom_msg.header.stamp = now
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_footprint'
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.orientation = q
        odom_msg.twist.twist.linear.x = self.vx
        odom_msg.twist.twist.linear.y = self.vy
        odom_msg.twist.twist.angular.z = self.vtheta
        self.odom_pub.publish(odom_msg)


def main(args=None):
    rclpy.init(args=args)
    node = OdomNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
