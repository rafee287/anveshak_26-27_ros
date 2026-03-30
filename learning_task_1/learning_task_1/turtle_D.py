import rclpy 
from rclpy.node import Node
from turtlesim.msg import Pose 
from geometry_msgs.msg import Twist

class TurtleD(Node):

    def __init__(self):
        super().__init__("turtle_D")
        self.get_logger().info("turtle_D has started")
        self.pose_subscriber = self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.cmd_vel_publisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10)

    def pose_callback(self, msg:Pose):
        cmd_vel = Twist()
        if(msg.x < 9.5 and msg.y > 5 and msg.y<5.6 and msg.theta > -0.01 and msg.theta < 0.01):
            cmd_vel.linear.x = 3.0
        elif(msg.x > 9.5 and msg.theta < 1.5708):
            cmd_vel.angular.z = 1.0
        elif(msg.theta > 1.5708 or msg.theta < -1.5708):
            cmd_vel.angular.z = 0.7
            cmd_vel.linear.x = 3.0
        elif(msg.theta > -1.5708 and msg.theta <-0.01 and msg.x < 1.0):
            cmd_vel.angular.z = 1.0
        self.cmd_vel_publisher.publish(cmd_vel)
        self.get_logger().info("current_pose is " + str(msg.x) + "," + str(msg.y) + "," + str(msg.theta))

def main(args = None):
    rclpy.init(args = args)
    node = TurtleD()
    rclpy.spin(node)
    rclpy.shutdown()