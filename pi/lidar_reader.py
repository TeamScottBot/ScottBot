import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarReader(Node):
    def __init__(self):
        super().__init__('lidar_reader')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

    def scan_callback(self, msg):

        
        valid_ranges = [r for r in msg.ranges if 0.1 < r < 12.0]
        
        if valid_ranges:
            # Find the absolute closest object to the LiDAR right now
            closest_distance = min(valid_ranges)
            
            # Print a specific warning if something gets within half a meter
            if closest_distance < 0.5:
                self.get_logger().info(f"🚨 WARNING! Object very close: {closest_distance:.2f} meters away!")
            else:
                self.get_logger().info(f"Path clear. Closest object is {closest_distance:.2f} meters away.")

def main(args=None):
    rclpy.init(args=args)
    lidar_reader = LidarReader()
    
    try:
        rclpy.spin(lidar_reader) 
    except KeyboardInterrupt:
        pass
    finally:
        lidar_reader.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()