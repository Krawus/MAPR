import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2


class OctomapSubscriber(Node):
    def __init__(self):
        super().__init__('octomap_subscriber')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/octomap_point_cloud_centers',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, cloud_msg):
        self.get_logger().info('I heard a pointcloud')
        gen = point_cloud2.read_points(cloud_msg)
        for points in gen:
            print(points)

def main(args=None):
   rclpy.init(args=args)
   octomap_subscriber = OctomapSubscriber()
   rclpy.spin(octomap_subscriber)
   octomap_subscriber.destroy_node()

   rclpy.shutdown()


if __name__ == '__main__':
   main()

