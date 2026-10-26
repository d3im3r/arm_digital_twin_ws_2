import os
import random

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, OpaqueFunction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


ARM_MODELS = ('moveo', 'mitsubishi', 'generic', 'franka')


def launch_setup(context):
    arm_model = LaunchConfiguration('arm_model').perform(context)
    if arm_model not in ARM_MODELS:
        valid_models = ', '.join(ARM_MODELS)
        raise ValueError(
            f"arm_model must be one of: {valid_models}; received '{arm_model}'"
        )

    pkg = get_package_share_directory('arm_digital_twin')
    arm_dof = 7 if arm_model == 'franka' else 3
    xacro_file = os.path.join(pkg, 'urdf', 'arm_digital_twin.urdf.xacro')
    rviz_cfg = os.path.join(pkg, 'rviz', 'arm_digital_twin.rviz')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file, ' arm_model:=', arm_model]),
        value_type=str
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    desc_pub = Node(
        package='arm_digital_twin',
        executable='robot_description_pub',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    bridge = Node(
        package='arm_digital_twin',
        executable='cmd_to_joint_states',
        output='screen',
        parameters=[{'arm_dof': arm_dof}]
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_cfg]
    )

    return [LogInfo(msg=f'Selected visual model: {arm_model}'), rsp, desc_pub, bridge, rviz]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'arm_model',
            default_value=random.choice(ARM_MODELS),
            description='Model: moveo, mitsubishi, generic (3 DOF), or franka (7 DOF)'
        ),
        OpaqueFunction(function=launch_setup)
    ])
