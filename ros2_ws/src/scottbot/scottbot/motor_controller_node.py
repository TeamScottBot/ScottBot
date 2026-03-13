import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from REVHubInterface.REVcomm import REVcomm

MAX_POWER = 16000
MOTOR_0_TRIM = 3200  # motor 0 runs slower


class MotorControllerNode(Node):
    def __init__(self, module):
        super().__init__('motor_controller_node')

        self.module = module
        self.blocked = False

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
        if self.blocked:
            self.get_logger().info('Ignoring cmd_vel – blocked')
            return

        lx = msg.linear.x
        ly = msg.linear.y
        az = msg.angular.z

        fl = lx + ly + az
        rl = lx - ly + az
        fr = lx - ly - az
        rr = lx + ly - az

        max_val = max(abs(fl), abs(rl), abs(fr), abs(rr), 1.0)
        fl /= max_val
        rl /= max_val
        fr /= max_val
        rr /= max_val

        powers = [
            int(fl * (MAX_POWER + MOTOR_0_TRIM)),
            int(rl * MAX_POWER),
            int(-fr * MAX_POWER),
            int(-rr * MAX_POWER),
        ]

        for i in range(4):
            self.module.motors[i].setMode(0, 1)
            self.module.motors[i].enable()
            self.module.motors[i].setPower(powers[i])

        self.get_logger().debug(
            f'cmd_vel: lx={lx:.2f} ly={ly:.2f} az={az:.2f} powers={powers}'
        )

    def _stop_motors(self):
        for i in range(4):
            self.module.motors[i].setPower(0)


def main(args=None):
    comm = REVcomm()
    comm.openActivePort()
    modules = comm.discovery()
    module = modules[0]

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
