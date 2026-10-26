import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class CmdToJointStates(Node):
    def __init__(self, arm_dof: int | None = None):
        super().__init__('cmd_to_joint_states_stage4')

        default_dof = 3 if arm_dof is None else arm_dof
        self.declare_parameter('arm_dof', default_dof)
        joint_count = self.get_parameter('arm_dof').get_parameter_value().integer_value
        if joint_count not in (3, 7):
            raise ValueError(f'arm_dof must be 3 or 7; received {joint_count}')

        # Publica el "estado" que consume robot_state_publisher
        self.pub = self.create_publisher(JointState, '/joint_states', 10)

        # Recibe comandos desde ESP32 o terminal
        self.sub = self.create_subscription(JointState, '/arm_cmd', self.cb, 10)

        # IMPORTANTE:
        # - Aquí se define QUÉ joints controla este stage.
        # - Los nombres deben coincidir con el URDF.
        self.joint_names = [
            f'joint{index}' for index in range(1, joint_count + 1)
        ] + ['gripper_joint', 'gripper_joint_mirror']
        self.arm_joint_names = self.joint_names[:-2]
        self.gripper_max_position = 0.04
        self.last_pos = [0.0] * len(self.joint_names)
        self.idx_grip_left = self.joint_names.index('gripper_joint')
        self.idx_grip_right = self.joint_names.index('gripper_joint_mirror')

        # Publicación periódica (30 Hz) -> robot "vivo" en RViz
        self.timer = self.create_timer(1.0/30.0, self.tick)

    def cb(self, msg: JointState):

        if not msg.name or not msg.position:
            return

        m = dict(zip(msg.name, msg.position))

        for i, jn in enumerate(self.arm_joint_names):
            if jn in m:
                self.last_pos[i] = float(m[jn])

        gripper_command = m.get('gripper_joint', m.get('gripper_joint_mirror'))
        if gripper_command is not None:
            val = float(gripper_command)
            clamped_val = min(self.gripper_max_position, max(0.0, val))
            if clamped_val != val:
                self.get_logger().warning(
                    f'Gripper position {val} is outside [0.0, '
                    f'{self.gripper_max_position}]; clamping to {clamped_val}.'
                )
            val = clamped_val
            self.last_pos[self.idx_grip_left] = val
            self.last_pos[self.idx_grip_right] = val

    def tick(self):
        out = JointState()
        out.header.stamp = self.get_clock().now().to_msg()
        out.name = self.joint_names
        out.position = self.last_pos
        self.pub.publish(out)


def main():
    rclpy.init()
    node = CmdToJointStates()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
