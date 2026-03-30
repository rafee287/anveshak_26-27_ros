# #!/usr/bin/env python3
# import rclpy 
# from rclpy.node import Node
# from std_msgs.msg import Int8

# class CountNode(Node):
    
#     def __init__(self):
#         super().__init__("counter_node")
#         self.get_logger().info("count_node started")
#         self.number_subscriber = self.create_subscription(Int8,"/number",self.number_recieved_callback, 10)
#         self.counter = 0
#         self.count_publisher = self.create_publisher(Int8,"/count",10)
#         # self.numbers = {}
#         self.current_number = None 

#     def number_recieved_callback(self, msg:Int8):

#         # if msg.data not in self.numbers.keys() :
#         #     self.numbers[msg] = 0
#         # else:
#         #     self.numbers[msg] +=1

#         received_val = msg.data 
#         if received_val == self.current_number:
#             self.counter += 1
#         else:
#             self.current_number = received_val
#             self.counter = 1
#         self.get_logger().info("counter_value: " + str(self.counter) + "and the number recived is " + str(msg.data))
#         publish_value = Int8()
#         publish_value.data = self.counter
#         self.count_publisher.publish(publish_value)
#         self.get_logger().info("the number published is (count):" + str(publish_value.data))

# def main(args = None):
#     rclpy.init(args = args)
#     node = CountNode()
#     rclpy.spin(node)
#     rclpy.shutdown()

#!/usr/bin/env python3
import rclpy 
from rclpy.node import Node
from std_msgs.msg import Int8

class CountNode(Node):
    
    def __init__(self):
        super().__init__("counter_node")
        self.get_logger().info("count_node started")
        
        self.number_subscriber = self.create_subscription(Int8, "/number", self.number_recieved_callback, 10)
        self.count_publisher = self.create_publisher(Int8, "/count", 10)
        
        self.counter = 0
        self.current_number = None 
        
        self.timer = self.create_timer(0.5, self.publish_timer_callback)

    def number_recieved_callback(self, msg: Int8):

        received_val = msg.data 
        if received_val == self.current_number:
            self.counter += 1
        else:
            self.current_number = received_val
            self.counter = 1
            
        self.get_logger().info("counter_value: " + str(self.counter) + " and the number received is " + str(msg.data))

    def publish_timer_callback(self):

        if self.current_number is not None:
            publish_value = Int8()
            publish_value.data = self.counter
            self.count_publisher.publish(publish_value)
            self.get_logger().info("the number published is (count):" + str(publish_value.data))

def main(args=None):
    rclpy.init(args=args)
    node = CountNode()
    rclpy.spin(node)
    rclpy.shutdown()

