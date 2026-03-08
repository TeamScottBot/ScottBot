# ROS 2 node that runs A* on a YAML map and publishes the path + commands
# publishes:  /planned_path (Path)  and  /nav_commands (JSON string)
# listens to: /replan (Empty) to re-run planning

from __future__ import annotations

import json

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from std_msgs.msg import Empty, String

from scottbot.astar import (
    astar,
    grid_to_world,
    inflate_grid,
    load_map,
    path_to_commands,
    simplify_path,
)


class AStarPlannerNode(Node):

    def __init__(self) -> None:
        super().__init__("astar_planner_node")

        # params — set these when you launch the node
        self.declare_parameter("map_file", "")
        self.declare_parameter("start", [0, 0])
        self.declare_parameter("goal", [0, 0])
        self.declare_parameter("robot_radius_cells", 2)
        self.declare_parameter("initial_heading_deg", 90.0)
        self.declare_parameter("cell_size_override", 0.0)  # 0 = use map's resolution

        # latched so if another node subscribes late it still gets the last msg
        latched_qos = QoSProfile(
            depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL
        )

        self._path_pub = self.create_publisher(
            Path, "/planned_path", latched_qos
        )
        self._cmd_pub = self.create_publisher(
            String, "/nav_commands", latched_qos
        )

        # publish Empty to /replan to trigger a new plan
        self.create_subscription(Empty, "/replan", self._on_replan, 10)

        # plan immediately on startup
        self._plan()

    def _on_replan(self, _msg: Empty) -> None:
        self.get_logger().info("Replan requested")
        self._plan()

    def _plan(self) -> None:
        map_file: str = self.get_parameter("map_file").value
        start = tuple(self.get_parameter("start").value)
        goal = tuple(self.get_parameter("goal").value)
        radius: int = self.get_parameter("robot_radius_cells").value
        heading: float = self.get_parameter("initial_heading_deg").value
        cell_override: float = self.get_parameter("cell_size_override").value

        if not map_file:
            self.get_logger().error("Parameter 'map_file' is not set")
            return

        # load the yaml map
        try:
            map_data = load_map(map_file)
        except Exception as exc:
            self.get_logger().error(f"Failed to load map: {exc}")
            return

        grid = map_data["grid"]
        resolution = map_data["resolution"]
        origin = tuple(map_data["origin"])
        cell_size = cell_override if cell_override > 0 else resolution
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        self.get_logger().info(
            f"Map {rows}x{cols}, res={resolution}m  "
            f"start={start} goal={goal} inflate_r={radius}"
        )

        # fatten walls so the robot doesn't clip them
        planning_grid = inflate_grid(grid, radius)

        # run A*
        try:
            path = astar(planning_grid, start, goal)
        except ValueError as exc:
            self.get_logger().error(f"A* error: {exc}")
            return

        if path is None:
            self.get_logger().error("A* found no path — goal is unreachable")
            return

        self.get_logger().info(f"Path found: {len(path)} cells")

        # convert path to TURN/FORWARD commands
        commands = path_to_commands(
            path, cell_size=cell_size, initial_heading=heading
        )

        self.get_logger().info(f"Generated {len(commands)} command(s):")
        for cmd_type, value in commands:
            unit = "\u00b0" if cmd_type == "TURN" else "m"
            self.get_logger().info(f"  {cmd_type:>7s}  {value:>8.3f}{unit}")

        # publish Path msg so we can see it in RViz
        path_msg = Path()
        path_msg.header.frame_id = "map"
        path_msg.header.stamp = self.get_clock().now().to_msg()

        for cell in simplify_path(path):
            ps = PoseStamped()
            ps.header = path_msg.header
            wx, wy = grid_to_world(cell, resolution, origin)
            ps.pose.position.x = wx
            ps.pose.position.y = wy
            path_msg.poses.append(ps)

        self._path_pub.publish(path_msg)

        # publish commands as JSON on /nav_commands
        cmd_dicts = [{"type": t, "value": v} for t, v in commands]
        cmd_msg = String()
        cmd_msg.data = json.dumps(cmd_dicts)
        self._cmd_pub.publish(cmd_msg)

        self.get_logger().info("Path and commands published")


def main(args=None):
    rclpy.init(args=args)
    node = AStarPlannerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
