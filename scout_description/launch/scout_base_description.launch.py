import os
import launch
import launch_ros

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, AppendEnvironmentVariable
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import FindExecutable, PathJoinSubstitution
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():

    scout_share = get_package_share_directory('scout_description')
    model_root = os.path.dirname(scout_share)
    
    model_name = 'scout_v2/scout_v2.xacro'
    # model_path = os.path.join(get_package_share_directory('scout_description'), "urdf", model_name)
    # print(model_path)
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        PathJoinSubstitution(
            [FindPackageShare("scout_description"), "urdf", model_name]
        ),
    ])

    return launch.LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true',
            description='Use simulation clock if true'),

        launch.actions.LogInfo(msg='use_sim_time: '),
        launch.actions.LogInfo(msg=launch.substitutions.LaunchConfiguration('use_sim_time')),
        
        #---test 
        # --- Make Gazebo able to resolve model://scout_description/... ---
        AppendEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=model_root + os.pathsep
        ),
        AppendEnvironmentVariable(
            name='IGN_GAZEBO_RESOURCE_PATH',
            value=model_root + os.pathsep
        ),
        
        launch_ros.actions.Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': launch.substitutions.LaunchConfiguration('use_sim_time'),
                'robot_description':robot_description_content
            }]),
    ])
