"""Delivery node – sends the robot between named waypoints (kitchen, living room, etc.).

Publishes navigation goals via the Nav2 NavigateToPose action.

Waypoints are defined in the WAYPOINTS dict below. After mapping your space,
open the map in RViz, hover over the kitchen and living room locations, and
record the (x, y, yaw) coordinates here.

Usage:
    ros2 run scottbot delivery_node --ros-args -p target:=living_room
    ros2 run scottbot delivery_node --ros-args -p target:=kitchen
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, Quaternion
from action_msgs.msg import GoalStatus


# ── Edit these after mapping your space ──────────────────────────────
# Coordinates are in the map frame (meters / radians).
# Find them by hovering in RViz over the map with the "2D Pose Estimate" tool.
WAYPOINTS = {
    'kitchen':     {'x':  1.0,  'y': -2.5,  'yaw': 0.0},
    'living_room': {'x': -0.5,  'y':  3.5,  'yaw': 1.57},
    'home':        {'x':  1.0,  'y': -2.5,  'yaw': 0.0},
}


def yaw_to_quaternion(yaw: float) -> Quaternion:
    q = Quaternion()
    q.z = math.sin(yaw / 2.0)
    q.w = math.cos(yaw / 2.0)
    return q


class DeliveryNode(Node):

    def __init__(self):
        super().__init__('delivery_node')

        self.declare_parameter('target', 'living_room')
        self.target = self.get_parameter('target').get_parameter_value().string_value

        if self.target not in WAYPOINTS:
            self.get_logger().error(
                f'Unknown target "{self.target}". '
                f'Valid targets: {list(WAYPOINTS.keys())}'
            )
            raise SystemExit(1)

        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.get_logger().info(f'Delivery node started – target: {self.target}')

        self._send_goal()

    def _send_goal(self):
        wp = WAYPOINTS[self.target]
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = wp['x']
        goal_msg.pose.pose.position.y = wp['y']
        goal_msg.pose.pose.orientation = yaw_to_quaternion(wp['yaw'])

        self.get_logger().info(
            f'Waiting for Nav2 action server...'
        )
        self._action_client.wait_for_server()

        self.get_logger().info(
            f'Navigating to {self.target} '
            f'(x={wp["x"]:.2f}, y={wp["y"]:.2f}, yaw={wp["yaw"]:.2f})'
        )
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self._feedback_cb
        )
        self._send_goal_future.add_done_callback(self._goal_response_cb)

    def _goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected by Nav2')
            raise SystemExit(1)

        self.get_logger().info('Goal accepted – navigating...')
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self._result_cb)

    def _feedback_cb(self, feedback_msg):
        pos = feedback_msg.feedback.current_pose.pose.position
        self.get_logger().info(
            f'  position: ({pos.x:.2f}, {pos.y:.2f})',
            throttle_duration_sec=2.0,
        )

    def _result_cb(self, future):
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(
                f'Arrived at {self.target}!'
            )
        else:
            self.get_logger().warn(
                f'Navigation failed with status: {status}'
            )
        raise SystemExit(0)


def main(args=None):
    rclpy.init(args=args)
    node = DeliveryNode()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
