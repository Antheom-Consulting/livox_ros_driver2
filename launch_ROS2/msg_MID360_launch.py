import os, json, sys
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
xfer_format     = 1 #1 for custom msg, 0 for 29doflauncher
multi_topic     = 0
data_src        = 0
publish_freq    = 10.0
output_type     = 0
frame_id        = 'mid360_link'
lvx_file_path   = '/home/livox/livox_test.lvx'
cmdline_bd_code = 'livox0000000001'
cur_path        = os.path.split(os.path.realpath(__file__))[0] + '/'
cur_config_path = cur_path + '../config'
config_path     = os.path.join(cur_config_path, 'MID360_config.json')
# host = laptop (always 192.168.123.100)
# lidar = LiDAR unit IP
# robot: LiDAR is at 192.168.123.200
# dolly: LiDAR is at 192.168.123.120
CONFIGS = {
    'robot': {'host': '192.168.123.100', 'lidar': '192.168.123.120'},
    'dolly': {'host': '192.168.123.100', 'lidar': '192.168.123.120'},
}
def generate_launch_description():
    mode = 'robot'
    for arg in sys.argv:
        if arg.startswith('mode:='):
            mode = arg.split(':=')[1]
    ips = CONFIGS.get(mode, CONFIGS['robot'])
    print(f'[MID360] mode={mode}  host={ips["host"]}  lidar={ips["lidar"]}')
    with open(config_path, 'r') as f:
        cfg = json.load(f)
    h = cfg['MID360']['host_net_info']
    h['cmd_data_ip']   = ips['host']
    h['push_msg_ip']   = ips['host']
    h['point_data_ip'] = ips['host']
    h['imu_data_ip']   = ips['host']
    cfg['lidar_configs'][0]['ip'] = ips['lidar']
    tmp_config = '/tmp/MID360_config_active.json'
    with open(tmp_config, 'w') as f:
        json.dump(cfg, f, indent=2)
    livox_ros2_params = [
        {"xfer_format": xfer_format},
        {"multi_topic": multi_topic},
        {"data_src": data_src},
        {"publish_freq": publish_freq},
        {"output_data_type": output_type},
        {"frame_id": frame_id},
        {"lvx_file_path": lvx_file_path},
        {"user_config_path": tmp_config},
        {"cmdline_input_bd_code": cmdline_bd_code}
    ]
    livox_driver = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_lidar_publisher',
        output='screen',
        parameters=livox_ros2_params
    )
    return LaunchDescription([
        DeclareLaunchArgument('mode', default_value='robot',
                              description='robot or dolly'),
        livox_driver,
    ])
