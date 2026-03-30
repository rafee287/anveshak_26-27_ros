# #!/usr/bin/env python3
# import rclpy 
# from rclpy.node import Node
# from std_msgs.msg import Int8

# class NumberNode (Node):
    
#     def __init__(self):
#         super().__init__("number_node")
#         self.get_logger().info("number_node started")
#         self.start_timer = self.create_timer(1,self.time_less_than_zero)
#         self.number_subscriber = self.create_subscription(Int8,"/count",self.count_recieved_callback, 10)
#         self.n = 0
#         self.count_publisher = self.create_publisher(Int8,"/number",10)

#     def count_recieved_callback(self,msg:Int8):
#         value = Int8()
#         self.get_logger().info("recieved count: " + str(msg.data))

#         # if self.n > 5:
#         #     while (1):
#         #         pass 

#         if self.n == 0 and msg.data == 1:
#             msg.data = 0

#         if msg.data == self.n:
#             self.n +=1
        
#         value.data = self.n 
#         self.count_publisher.publish(value)
#         self.get_logger().info("sending value: " + str(value.data))
    
#     def time_less_than_zero(self):
#         value = Int8()
#         value.data = self.n
#         self.get_logger().info("publishing value " +str(value.data) + " because t<0")
#         self.count_publisher.publish(value)
#         if self.count_publisher.get_subscription_count() > 0:
#             self.start_timer.cancel()

# def main(args = None):
#     rclpy.init(args = args)
#     node = NumberNode()
#     rclpy.spin(node)
#     rclpy.shutdown()

#!/usr/bin/env python3
import rclpy 
from rclpy.node import Node
from std_msgs.msg import Int8

class NumberNode(Node):
    
    def __init__(self):
        super().__init__("number_node")
        self.get_logger().info("number_node started")
        
        self.number_subscriber = self.create_subscription(Int8, "/count", self.count_recieved_callback, 10)
        self.count_publisher = self.create_publisher(Int8, "/number", 10)
        
        self.n = 0
        
        self.timer = self.create_timer(0.5, self.publish_timer_callback)

    def count_recieved_callback(self, msg: Int8):

        received_val = msg.data
        self.get_logger().info("received count: " + str(received_val))

        if self.n == 0 and received_val == 1:
            received_val = 0

        if received_val == self.n:
            self.n += 1
            
    def publish_timer_callback(self):

        value = Int8()
        value.data = self.n 
        self.count_publisher.publish(value)
        self.get_logger().info("sending value: " + str(value.data))

def main(args=None):
    rclpy.init(args=args)
    node = NumberNode()
    rclpy.spin(node)
    rclpy.shutdown()
