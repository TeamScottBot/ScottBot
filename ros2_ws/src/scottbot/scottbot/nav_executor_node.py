from __future__ import annotations

import json
import math
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class NavExecutorNode(Node):

    def __init__(self):
        super().__init__('nav_executor_node')

        self.declare_parameter('linear_speed', 0.15)   # m/s actual robot speed
        self.declare_parameter('angular_speed', 0.4)    # rad/s actual turn speed
        self.declare_parameter('cmd_linear', 0.3)       # cmd_vel linear.x to send
        self.declare_parameter('cmd_angular', 0.5)      # cmd_vel angular.z to send
        self.declare_parameter('pause_between', 0.5)    # seconds pause between cmds

        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        self.cmd_linear = self.get_parameter('cmd_linear').value
        self.cmd_angular = self.get_parameter('cmd_angular').value
        self.pause_between = self.get_parameter('pause_between').value

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(String, '/nav_commands', self._on_commands, 10)

        self.get_logger().info(
            f'NavExecutor ready (linear={self.linear_speed} m/s, '
            f'angular={self.angular_speed} rad/s)'
        )

    def _stop(self):
        self.cmd_pub.publish(Twist())

    def _on_commands(self, msg: String):
        try:
            commands = json.loads(msg.data)
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Bad JSON: {e}')
            return

        merged = []
        for cmd in commands:
            if (merged
                    and merged[-1]['type'] == cmd['type']
                    and cmd['type'] == 'FORWARD'):
                merged[-1]['value'] += cmd['value']
            elif cmd['type'] == 'TURN' and merged and merged[-1]['type'] == 'TURN':
                merged[-1]['value'] += cmd['value']
            else:
                merged.append(dict(cmd))

        merged = [c for c in merged
                  if not (c['type'] == 'FORWARD' and abs(c['value']) < 0.05)
                  and not (c['type'] == 'TURN' and abs(c['value']) < 5.0)]

        self.get_logger().info(
            f'Executing {len(merged)} commands (merged from {len(commands)})'
        )

        for i, cmd in enumerate(merged):
            cmd_type = cmd['type']
            value = cmd['value']

            if cmd_type == 'TURN':
                self._execute_turn(value, i + 1, len(merged))
            elif cmd_type == 'FORWARD':
                self._execute_forward(value, i + 1, len(merged))
            else:
                self.get_logger().warn(f'Unknown command: {cmd_type}')
                continue

            self._stop()
            time.sleep(self.pause_between)

        self._stop()
        self.get_logger().info('All commands executed — arrived at goal')

    def _execute_turn(self, degrees: float, idx: int, total: int):
        radians = math.radians(degrees)
        duration = abs(radians) / self.angular_speed
        direction = 1.0 if radians > 0 else -1.0

        self.get_logger().info(
            f'[{idx}/{total}] TURN {degrees:.1f}° ({duration:.2f}s)'
        )

        twist = Twist()
        twist.angular.z = direction * self.cmd_angular

        end_time = time.time() + duration
        while time.time() < end_time:
            self.cmd_pub.publish(twist)
            time.sleep(0.05)

    def _execute_forward(self, meters: float, idx: int, total: int):
        duration = meters / self.linear_speed

        self.get_logger().info(
            f'[{idx}/{total}] FORWARD {meters:.3f}m ({duration:.2f}s)'
        )

        twist = Twist()
        twist.linear.x = self.cmd_linear

        end_time = time.time() + duration
        while time.time() < end_time:
            self.cmd_pub.publish(twist)
            time.sleep(0.05)


def main(args=None):
    rclpy.init(args=args)
    node = NavExecutorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node._stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
