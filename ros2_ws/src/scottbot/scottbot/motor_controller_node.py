"""Motor controller node – subscribes to /blocked and /cmd_vel to drive the motors."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from REVHubInterface.REVcomm import REVcomm

MAX_POWER = 32000


class MotorControllerNode(Node):
    """Drives mecanum motors based on velocity commands, with emergency stop from /blocked."""

    def __init__(self, module):
        super().__init__('motor_controller_node')

        self.module = module
        self.blocked = False

        # Initialize all 4 motors
        for i in range(4):
            self.module.motors[i].setMode(0, 1)
            self.module.motors[i].enable()

        self.blocked_sub = self.create_subscription(
            Bool, '/blocked', self.blocked_callback, 10
        )
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10
        )
        self.get_logger().info('MotorControllerNode started (REV Hub connected)')

    def blocked_callback(self, msg: Bool):
        self.blocked = msg.data
        if self.blocked:
            self.get_logger().warn('Obstacle detected – stopping motors')
            self._stop_motors()

    def cmd_vel_callback(self, msg: Twist):
        print("Received cmd_vel:", msg)
        if self.blocked:
            self.get_logger().info('Ignoring cmd_vel – blocked')
            return

        linear_x = msg.linear.x    # forward/backward
        linear_y = msg.linear.y    # strafe left/right (mecanum)
        angular_z = msg.angular.z  # rotation

        # Movement logic matching lidar_reader.py
        if linear_x > 0 and linear_y == 0 and angular_z == 0:
            # Forward
            for i in range(2):
                self.module.motors[i].setMode(0, 1)
                self.module.motors[i].enable()
                self.module.motors[i].setPower(MAX_POWER)
            for i in range(2, 4):
                self.module.motors[i].setMode(0, 1)
                self.module.motors[i].enable()
                self.module.motors[i].setPower(-MAX_POWER)
        elif linear_x < 0 and linear_y == 0 and angular_z == 0:
            # Backward
            for i in range(2):
                self.module.motors[i].setMode(0, 1)
                self.module.motors[i].enable()
                self.module.motors[i].setPower(-MAX_POWER)
            for i in range(2, 4):
                self.module.motors[i].setMode(0, 1)
                self.module.motors[i].enable()
                self.module.motors[i].setPower(MAX_POWER)
        elif linear_x > 0 and linear_y > 0:
            # Diagonal left forward
            self.module.motors[0].setMode(0, 1)
            self.module.motors[0].enable()
            self.module.motors[0].setPower(MAX_POWER)
            self.module.motors[2].setMode(0, 1)
            self.module.motors[2].enable()
            self.module.motors[2].setPower(-MAX_POWER)
            self.module.motors[1].setPower(0)
            self.module.motors[3].setPower(0)
        elif linear_x > 0 and linear_y < 0:
            # Diagonal right forward
            self.module.motors[1].setMode(0, 1)
            self.module.motors[1].enable()
            self.module.motors[1].setPower(MAX_POWER)
            self.module.motors[3].setMode(0, 1)
            self.module.motors[3].enable()
            self.module.motors[3].setPower(-MAX_POWER)
            self.module.motors[0].setPower(0)
            self.module.motors[2].setPower(0)
        elif linear_y > 0:
            # Left
            self.module.motors[0].setMode(0, 1)
            self.module.motors[0].enable()
            self.module.motors[0].setPower(-MAX_POWER)
            self.module.motors[2].setMode(0, 1)
            self.module.motors[2].enable()
            self.module.motors[2].setPower(-MAX_POWER)
            self.module.motors[1].setMode(0, 1)
            self.module.motors[1].enable()
            self.module.motors[1].setPower(MAX_POWER)
            self.module.motors[3].setMode(0, 1)
            self.module.motors[3].enable()
            self.module.motors[3].setPower(MAX_POWER)
        elif linear_y < 0:
            # Right
            self.module.motors[0].setMode(0, 1)
            self.module.motors[0].enable()
            self.module.motors[0].setPower(MAX_POWER)
            self.module.motors[2].setMode(0, 1)
            self.module.motors[2].enable()
            self.module.motors[2].setPower(MAX_POWER)
            self.module.motors[1].setMode(0, 1)
            self.module.motors[1].enable()
            self.module.motors[1].setPower(-MAX_POWER)
            self.module.motors[3].setMode(0, 1)
            self.module.motors[3].enable()
            self.module.motors[3].setPower(-MAX_POWER)
        elif angular_z > 0:
            # Rotate left
            for i in range(4):
                self.module.motors[i].setMode(0, 1)
                self.module.motors[i].enable()
                self.module.motors[i].setPower(MAX_POWER)
        elif angular_z < 0:
            # Rotate right
            for i in range(4):
                self.module.motors[i].setMode(0, 1)
                self.module.motors[i].enable()
                self.module.motors[i].setPower(-MAX_POWER)
        else:
            # Stop
            for i in range(4):
                self.module.motors[i].setPower(0)

        self.get_logger().debug(
            f'cmd_vel: lx={linear_x:.2f} ly={linear_y:.2f} az={angular_z:.2f}'
        )

        linear_x = msg.linear.x    # forward/backward
        linear_y = msg.linear.y    # strafe left/right (mecanum)
        angular_z = msg.angular.z  # rotation

        # Mecanum inverse kinematics: compute per-wheel power
        # Motors 0,1 = left-front, left-rear
        # Motors 2,3 = right-front, right-rear
        front_left = linear_x + linear_y + angular_z
        rear_left = linear_x - linear_y + angular_z
        front_right = linear_x - linear_y - angular_z
        rear_right = linear_x + linear_y - angular_z

        # Normalize so no wheel exceeds 1.0
        max_val = max(abs(front_left), abs(rear_left),
                      abs(front_right), abs(rear_right), 1.0)
        front_left /= max_val
        rear_left /= max_val
        front_right /= max_val
        rear_right /= max_val

        # Right side is inverted (motors spin opposite direction)
        powers = [
            int(front_left * MAX_POWER),
            int(rear_left * MAX_POWER),
            int(-front_right * MAX_POWER),
            int(-rear_right * MAX_POWER),
        ]

        for i in range(4):
            self.module.motors[i].setPower(powers[i])

        self.get_logger().debug(
            f'cmd_vel: lx={linear_x:.2f} ly={linear_y:.2f} az={angular_z:.2f} '
            f'powers={powers}'
        )

    def _stop_motors(self):
        for i in range(4):
            self.module.motors[i].setPower(0)


def main(args=None):
    comm = REVcomm()
    comm.openActivePort()
    modules = comm.discovery()
    module = modules[0]
    print(f"REV Hub address: {module.getAddress()}")

    # TEST: drive forward for 1 second
    for i in range(4):
        module.motors[i].setMode(0, 1)
        module.motors[i].enable()
    # Left motors forward, right motors backward (mecanum convention)
    module.motors[0].setPower(12800)
    module.motors[1].setPower(12800)
    module.motors[2].setPower(-12800)
    module.motors[3].setPower(-12800)
    print("TEST: Driving forward for 1 second...")
    import time
    time.sleep(1)
    for i in range(4):
        module.motors[i].setPower(0)
    print("TEST: Motors stopped.")

    rclpy.init(args=args)
    node = MotorControllerNode(module)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node._stop_motors()
        node.destroy_node()
        rclpy.shutdown()
        comm.closeActivePort()


if __name__ == '__main__':
    main()
