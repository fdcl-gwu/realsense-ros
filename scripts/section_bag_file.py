import pdb
import rosbag
import rospy
import threading

from sensor_msgs.msg import Imu, Image


lock = threading.Lock()

bag = rosbag.Bag('test.bag', 'w')
accel_topic = '/device_0/sensor_2/Accel_0/imu/data'
gyro_topic = '/device_0/sensor_2/Gyro_0/imu/data'
image_topic = '/device_0/sensor_1/Color_0/image/data'


def callback_accel(data):
    with lock:
        bag.write(accel_topic, data)


def callback_gyro(data):
    with lock:
        bag.write(gyro_topic, data)


def callback_image(data):
    with lock:
        bag.write(image_topic, data)



def listener():
    rospy.Subscriber(accel_topic, Imu, callback_accel)
    rospy.Subscriber(gyro_topic, Imu, callback_gyro)
    rospy.Subscriber(image_topic, Image, callback_image)
    
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('section_bag_node', anonymous=True)

    try:
        listener()
    finally:
        bag.close()
