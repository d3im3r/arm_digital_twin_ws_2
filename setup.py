from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'arm_digital_twin'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='d3im3r_rl',
    maintainer_email='demiranda@unal.edu.co',
    description='Stage4: RRR + gripper',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robot_description_pub = arm_digital_twin.robot_description_pub:main',
            'cmd_to_joint_states = arm_digital_twin.cmd_to_joint_states:main',
        ],
    },
)
