import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy
from std_msgs.msg import String

class RobotDescriptionPublisher(Node):
    def __init__(self):
        super().__init__('robot_description_publisher')

        # QoS "latched" (transient local) para que RViz lo reciba aunque se conecte después
        qos = QoSProfile(depth=1)
        qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        qos.reliability = ReliabilityPolicy.RELIABLE

        self.pub = self.create_publisher(String, '/robot_description', qos)

        # Declarar el parámetro (buena práctica y evita vacíos)
        self.declare_parameter('robot_description', '')

        desc = self.get_parameter('robot_description').get_parameter_value().string_value
        if not desc:
            self.get_logger().error("robot_description está vacío. Revisa el launch.")
            desc = "<robot name='empty'/>"

        # Guardar el mensaje para re-publicar
        self.msg = String()
        self.msg.data = desc

        # Publicación inicial
        self.pub.publish(self.msg)
        self.get_logger().info('Publicado /robot_description (latched).')

        # Re-publicar cada 1s (por si RViz arranca después o cambia de display)
        self.timer = self.create_timer(1.0, self.timer_cb)

    def timer_cb(self):
        self.pub.publish(self.msg)

def main():
    rclpy.init()
    node = RobotDescriptionPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()