#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose 
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial


class TurtleController(Node):
    
    def __init__(self):
        super().__init__("turtle_controller")
        self.get_logger().info("turlte_controller has started")
        self.previous_x = 0.0
        self.pose_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.cmd_vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

    
    def pose_callback(self,pose: Pose, X : float):
        # update velocity command based on the position of the turtle
        cmd = Twist() 
        if(pose.x <2 or pose.x>9 or pose.y >9 or pose. y < 2):
            cmd.linear.x = 1.0
            cmd.angular.z = 0.7
            
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0 
        self.cmd_vel_publisher.publish(cmd)

        if (pose.x>5.5 and self.previous_x<=5.5):
            self.previous_x = pose.x
            self.call_set_pen_service(255,0,0,3,0)
            self.get_logger().info("setting color to red")
        elif (pose.x<5.5 and self.previous_x>=5.5):
            self.previous_x = pose.x
            self.call_set_pen_service(0,255,0,3,0)
            self.get_logger().info("setting color to green")


    def call_set_pen_service(self,r,g,b,width,off):
        client = self.create_client(SetPen, "/turtle1/set_pen")
        while not client.wait_for_service(1.0):
            self.get_logger().info("waiting for service")

        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off
        
        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("service call failed: %r" % ( e,))


def main(args = None):
    rclpy.init(args = args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()