import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import numpy as np
from math import cos, sin, pi

class PathPublisher(Node):

    def __init__(self):
        super().__init__('path_publisher')
        self.publisher_ = self.create_publisher(Path, 'my_path', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.r = 0.7

    def timer_callback(self):
        path = Path()
        path.header.frame_id = 'odom'
        
        # create path
        theta = np.linspace(0, 2*pi, 50)

        for angle in theta:
            pose = PoseStamped()
            # circle
            pose.pose.position.x = 0.0
            pose.pose.position.y = self.r * cos(angle)
            pose.pose.position.z = 1 + self.r * sin(angle)

            pose.pose.orientation.x = 0.0
            pose.pose.orientation.y = 0.0
            pose.pose.orientation.z = 0.0
            pose.pose.orientation.w = 1.0
            pose.header.frame_id = 'odom'
            pose.header.stamp = self.get_clock().now().to_msg()
            path.poses.append(pose)
        
        #publish path
        self.publisher_.publish(path)
        self.get_logger().info('Publishing path')

def main(args=None):
    rclpy.init(args=args)
    path_publisher = PathPublisher()
    rclpy.spin(path_publisher)
    path_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
