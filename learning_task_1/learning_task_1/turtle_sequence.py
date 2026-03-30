#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtleSequence(Node):
    def __init__(self):
        super().__init__("turtle_sequence")
        
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        
        self.current_pose = None
        self.state = 0
        self.start_time = None
        
        self.timer = self.create_timer(0.02, self.control_loop)
        self.get_logger().info(" waiting to get a pose message ")

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

    def control_loop(self):
        if self.current_pose is None:
            return

        msg = Twist()
        now = self.get_clock().now()

        # state 0: moving forward from starting point with velocity 2 for 2 seconds
    
        if self.state == 0:
            if self.start_time is None:
                self.start_time = now
                self.get_logger().info("State 0: Moving forward (East)")
            
            elapsed = (now - self.start_time).nanoseconds / 1e9
            
            if elapsed < 2.0:
                msg.linear.x = 2.0
                self.cmd_vel_pub.publish(msg)
            else:
                self.start_time = None
                self.state = 1
                self.get_logger().info("the current x position is " + str(self.current_pose.x))

        # state 1 : turning left to make angle of pi/2

        elif self.state == 1:
            target_angle = 1.5708 # pi/2
            
            if abs(target_angle - self.current_pose.theta) > 0.05:
                msg.angular.z = 1.0  # spin left
                self.cmd_vel_pub.publish(msg)
            else:
                self.get_logger().info("State 1: Facing North. current_angle is " + str(self.current_pose.theta))
                self.state = 2

        # state 2: The semicircular path
        # radius = 4.0 moves from x=9.5 back to x=1.5

        elif self.state == 2:
            if self.start_time is None:
                self.start_time = now
                self.get_logger().info("State 2: Drawing the arc")
                
            elapsed = (now - self.start_time).nanoseconds / 1e9
            
            # t = pi *r / v = 3.14 * 4 / 2 = 6.28

            if elapsed < 6.28:
                msg.linear.x = 2.0
                msg.angular.z = 0.5 
                self.cmd_vel_pub.publish(msg)
            else:
                self.start_time = None
                self.state = 3
                self.get_logger().info("the end of arc is at " + str(self.current_pose.x) + "," + str(self.current_pose.y))
                self.get_logger().info("the end of arc is at angle " + str(self.current_pose.theta))

        # State 3: Turning Left to get theta = 0 agian

        elif self.state == 3:
            target_angle = 0.0
            
            if abs(target_angle - self.current_pose.theta) > 0.02:
                msg.angular.z = 1.0  # Spin Left
                self.cmd_vel_pub.publish(msg)
            else:

                self.get_logger().info("facing angle " + str(self.current_pose.theta))
                self.state = 4

        # State 4: move forward at theta = 0 (closing the D)
        # moving from x=1.5 back to x=5.5

        elif self.state == 4:
            if self.start_time is None:
                self.start_time = now
                self.get_logger().info("State 4: Closing the shape")
                
            elapsed = (now - self.start_time).nanoseconds / 1e9
            
            if elapsed < 2.0:
                msg.linear.x = 2.0
                self.cmd_vel_pub.publish(msg)
            else:
                self.get_logger().info("Shape Complete! Back at default position.")
                self.cmd_vel_pub.publish(Twist())   # stopping the motion by sending an empty command
                self.state = 5
                self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSequence()
    rclpy.spin(node)
    rclpy.shutdown()
