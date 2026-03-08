import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import LaserScan
from REVHubInterface.REVcomm import REVcomm
import time


class LidarReader(Node):
    def __init__(self, module):
        super().__init__('lidar_reader')
        self.module = module
        self.state = None  
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            sensor_qos)

        self.forward()

    def forward(self):
        for i in range(2):
            self.module.motors[i].setMode(0, 1)
            self.module.motors[i].enable()
            self.module.motors[i].setPower(12800)

        for i in range(2, 4):
            self.module.motors[i].setMode(0, 1)
            self.module.motors[i].enable()
            self.module.motors[i].setPower(-12800)

        print("ScottBot set to move forward!")

    def backward(self):
        for i in range(2):
            self.module.motors[i].setMode(0, 1)
            self.module.motors[i].enable()
            self.module.motors[i].setPower(-12800)

        for i in range(2, 4):
            self.module.motors[i].setMode(0, 1)
            self.module.motors[i].enable()
            self.module.motors[i].setPower(12800)
            print(f"Motor {i} started!")

    def diagonalRightForward(self):
        self.module.motors[1].setMode(0, 1)
        self.module.motors[1].enable()
        self.module.motors[1].setPower(12800)

        self.module.motors[3].setMode(0, 1)
        self.module.motors[3].enable()
        self.module.motors[3].setPower(-12800)

    def diagonalLeftForward(self):
        self.module.motors[0].setMode(0, 1)
        self.module.motors[0].enable()
        self.module.motors[0].setPower(12800)

        self.module.motors[2].setMode(0, 1)
        self.module.motors[2].enable()
        self.module.motors[2].setPower(-12800)

    def right(self):
        self.module.motors[0].setMode(0, 1)
        self.module.motors[0].enable()
        self.module.motors[0].setPower(12800)

        self.module.motors[2].setMode(0, 1)
        self.module.motors[2].enable()
        self.module.motors[2].setPower(12800)

        self.module.motors[1].setMode(0, 1)
        self.module.motors[1].enable()
        self.module.motors[1].setPower(-12800)

        self.module.motors[3].setMode(0, 1)
        self.module.motors[3].enable()
        self.module.motors[3].setPower(-12800)

    def left(self):
        self.module.motors[0].setMode(0, 1)
        self.module.motors[0].enable()
        self.module.motors[0].setPower(-12800)

        self.module.motors[2].setMode(0, 1)
        self.module.motors[2].enable()
        self.module.motors[2].setPower(-12800)

        self.module.motors[1].setMode(0, 1)
        self.module.motors[1].enable()
        self.module.motors[1].setPower(12800)

        self.module.motors[3].setMode(0, 1)
        self.module.motors[3].enable()
        self.module.motors[3].setPower(12800)

    def stop(self):
        for i in range(4):
            self.module.motors[i].setPower(0)
            self.module.motors[i].disable()
        self.state = 'stopped'
        print("ScottBot stopped!")

    def scan_callback(self, msg):
        valid_ranges = [r for r in msg.ranges if 0.1 < r < 12.0]

        if valid_ranges:
            closest_distance = min(valid_ranges)

            if closest_distance < 1.0:
                if self.state != 'stopped':
                    self.get_logger().info(f"🚨 WARNING! Object very close: {closest_distance:.2f} meters away!")
                    self.stop()
            else:
                if self.state != 'forward':
                    self.get_logger().info(f"Path clear. Closest object is {closest_distance:.2f} meters away.")
                    self.forward()


def main(args=None):

    comm = REVcomm()
    comm.openActivePort()

    modules = comm.discovery()
    module = modules[0]
    print(f"Hub address: {module.getAddress()}")

    rclpy.init(args=args)
    lidar_reader = LidarReader(module)
    
    try:
        rclpy.spin(lidar_reader) 
    except KeyboardInterrupt:
        pass
    finally:
        lidar_reader.destroy_node()
        rclpy.shutdown()


    comm.closeActivePort()
    print("Done.")


if __name__ == '__main__':
    main()
