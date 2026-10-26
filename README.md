<div align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://cdn.jsdelivr.net/gh/d3im3r/d3im3r-brand-assets@main/assets/svg/horizontal-dark.svg"
    />
    <img
      src="https://cdn.jsdelivr.net/gh/d3im3r/d3im3r-brand-assets@main/assets/svg/horizontal-light.svg"
      alt="d3im3r owl-chip brand"
      width="280"
    />
  </picture>
  <h1>Arm Digital Twin · v2</h1>
  <p><strong>A lightweight ROS 2 workspace for visualizing and testing articulated robot arms in RViz.</strong></p>
  <p>
    <img src="https://img.shields.io/badge/ROS%202-Humble-22314E?logo=ros" alt="ROS 2 Humble" />
    <img src="https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu&logoColor=white" alt="Ubuntu 22.04" />
    <img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python 3.10" />
    <img src="https://img.shields.io/badge/Visualization-RViz-5B8DEF" alt="RViz" />
  </p>
</div>

Arm Digital Twin turns ROS 2 joint commands into visible motion in RViz. Version 2 includes four selectable arm designs, a shared gripper, and a simple command interface for interactive testing or integration with an external ROS 2 node.

> Choose a model, publish joint positions, and watch the robot move in RViz.

## Features

- **Four robot designs:** three 3-DOF arms and one simplified 7-DOF Franka-style arm.
- **Selectable models:** choose a model explicitly or let the launch file select one at random.
- **Articulated gripper:** coordinated fingers with a command range of `0.0` to `0.04` m.
- **Distinct visual details:** model-specific proportions, colors, and fixed pivot accents.
- **Lightweight descriptions:** all current robot geometry is built from Xacro primitives; external CAD meshes are not required.
- **ROS 2 command bridge:** receives `sensor_msgs/msg/JointState` on `/arm_cmd` and publishes `/joint_states` for the robot state publisher and RViz.

## Robot models

| Model | Arm DOF | Description |
| --- | ---: | --- |
| `moveo` | 3 | Open-link design with paired rails |
| `generic` | 3 | Compact arm with simple geometry |
| `mitsubishi` | 3 | Industrial-style cylindrical bodies |
| `franka` | 7 | Simplified, articulated industrial arm |

Every model includes a gripper. For the 3-DOF models, `joint1`, `joint2`, and `joint3` control the base, shoulder, and elbow. The Franka-style model adds `joint4` through `joint7`.

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- `colcon`

Install the ROS packages used by the visualization:

```bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  ros-humble-rviz2 \
  ros-humble-xacro \
  ros-humble-robot-state-publisher
```

## Build and launch

Create a ROS 2 workspace, clone this repository into its `src` directory, and build:

```bash
mkdir -p ~/arm_digital_twin_ws/src
cd ~/arm_digital_twin_ws/src
git clone https://github.com/d3im3r/arm-digital-twin-v2.git arm_digital_twin

cd ~/arm_digital_twin_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Launch the visualizer with a randomly selected model:

```bash
ros2 launch arm_digital_twin display.launch.py
```

Or select a model explicitly:

```bash
ros2 launch arm_digital_twin display.launch.py arm_model:=moveo
ros2 launch arm_digital_twin display.launch.py arm_model:=generic
ros2 launch arm_digital_twin display.launch.py arm_model:=mitsubishi
ros2 launch arm_digital_twin display.launch.py arm_model:=franka
```

Stop the current launch with `Ctrl+C` before switching models.

## Test joint commands

Open another terminal and source both ROS 2 and the workspace:

```bash
source /opt/ros/humble/setup.bash
cd ~/arm_digital_twin_ws
source install/setup.bash
```

For a 3-DOF arm, publish three joint angles and a gripper command. Arm positions are in radians; the gripper position is in meters:

```bash
ros2 topic pub --once /arm_cmd sensor_msgs/msg/JointState \
"{name: ['joint1', 'joint2', 'joint3', 'gripper_joint'], position: [0.6, 0.4, 1.0, 0.03]}"
```

For the 7-DOF Franka-style arm:

```bash
ros2 topic pub --once /arm_cmd sensor_msgs/msg/JointState \
"{name: ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper_joint'], position: [0.0, -0.4, 0.0, -1.8, 0.0, 1.4, 0.7, 0.02]}"
```

You can also command a single joint:

```bash
ros2 topic pub --once /arm_cmd sensor_msgs/msg/JointState \
"{name: ['joint2'], position: [0.8]}"
```

The bridge retains the last position for joints omitted from a command. Gripper values are clamped to the range `0.0`–`0.04`: `0.0` closes the fingers and positive values open them. Both fingers move together.

## Data flow

```text
External ROS 2 node or terminal
              │
              ▼
       /arm_cmd (JointState)
              │
              ▼
      cmd_to_joint_states
              │
              ▼
       /joint_states ──► robot_state_publisher ──► RViz
```

An external hardware or micro-ROS node can publish compatible messages to `/arm_cmd`. Device transport and micro-ROS configuration are outside this package.

## Project layout

```text
arm_digital_twin/
├── arm_digital_twin/   # ROS 2 Python nodes
├── config/             # Controller configuration
├── launch/             # Model selection and RViz launch
├── resource/           # Ament package resource marker
├── rviz/               # RViz configuration
├── test/               # Package lint and style tests
└── urdf/               # Xacro robot description
```

Build outputs (`build/`, `install/`, and `log/`), Python bytecode caches, and unused reference CAD assets are not part of the project. The current models do not depend on external mesh files.

## Development

After changing the Xacro description, rebuild and launch a model:

```bash
cd ~/arm_digital_twin_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select arm_digital_twin
source install/setup.bash
ros2 launch arm_digital_twin display.launch.py arm_model:=moveo
```

## Scope

This project currently focuses on joint-command testing and visualization in RViz. Gazebo simulation and direct hardware communication are not included in the documented workflow.

## Brand attribution

The d3im3r logo is used with express written authorization from the asset owner. Brand assets are served from the [d3im3r brand assets repository](https://github.com/d3im3r/d3im3r-brand-assets) and are not redistributed in this repository. See the [authorization](https://github.com/d3im3r/d3im3r-brand-assets/issues/1#issuecomment-6404613664) and [brand usage guidelines](https://github.com/d3im3r/d3im3r-brand-assets/blob/main/BRAND.md).
