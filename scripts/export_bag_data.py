import rosbag
from geometry_msgs.msg import Point
import pandas as pd

# The bag file should be in the same directory as your terminal
bag = rosbag.Bag('./saved_pose.bag')
topic = '/vins_estimator/camera_pose/'
column_names = ['x',
                'y', 
                'z']
df = pd.DataFrame(columns=column_names)

for topic, msg, t in bag.read_messages(topics=topic):

    position = msg.pose.pose.position
    rotation = msg.pose.pose.orientation

    df = df.append(
        {'x': position.x,
         'y': position.y,
         'z': position.z,
         'qw': rotation.w,
         'qx': rotation.x,
         'qy': rotation.y,
         'qz': rotation.z},
        ignore_index=True
    )

df.to_csv('out.csv')
