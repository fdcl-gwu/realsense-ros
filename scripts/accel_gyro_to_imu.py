import rospy
import threading

from std_msgs.msg import String
from sensor_msgs.msg import Imu

imu = Imu()
lock = threading.Lock()

def talker():
    pub = rospy.Publisher('/camera/imu/data_raw', Imu, queue_size=10)
    rate = rospy.Rate(63)
    
    while not rospy.is_shutdown():
        pub.publish(imu)
        rate.sleep()


def callback_accel(data):
    with lock:
        imu.header.frame_id = data.header.frame_id
        imu.header.stamp = data.header.stamp
        imu.linear_acceleration.x = data.linear_acceleration.x
        imu.linear_acceleration.y = data.linear_acceleration.y
        imu.linear_acceleration.z = data.linear_acceleration.z


def callback_gyro(data):
    with lock:
        imu.header.frame_id = data.header.frame_id
        imu.header.stamp = data.header.stamp
        imu.angular_velocity.x = data.angular_velocity.x
        imu.angular_velocity.y = data.angular_velocity.y
        imu.angular_velocity.z = data.angular_velocity.z


def listener():
    rospy.Subscriber('/device_0/sensor_2/Accel_0/imu/data',
                     Imu, callback_accel)
    rospy.Subscriber('/device_0/sensor_2/Gyro_0/imu/data',
                     Imu, callback_gyro)


if __name__ == '__main__':
    rospy.init_node('imu_intermediate_node', anonymous=True)

    try:
        listener()
        talker()
    except rospy.ROSInterruptException:
        pass
