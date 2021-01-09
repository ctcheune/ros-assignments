#1. {what is the topic of the position?}
##Topic: /turtle1/pose
##Type: turtlesim/Pose
##Message Content: 
# float32 x
# float32 y
# float32 theta
# float32 linear_velocity
# float32 angular_velocity



#2. {what is the topic that makes the robot move?}
##Topic: /turtle1/cmd_vel
##Type: geometry_msgs/Twist
##Message Content:
#geometry_msgs/Vector3 linear
# float64 x
# float64 y
# float64 z
#geometry_msgs/Vector3 angular
# float64 x
# float64 y
# float64 z

#3. {Write a simple ROS program called turtlesim_pose.py, 
# which subscribes to the topic of the pose, and then prints
# the position of the robot in the callback function}

#Project: Assignment 1 
#Author: Coralie Tcheune
#Date: 01-07-2021

#import necessary modules
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

#define coordinates for robot's position 
x = 0
y = 0
z = 0
yaw = 0

#displays the coordinates of the robot
def poseCallback(pose_message):
    global x
    global y, z, yaw

    #display the x,y, and theta recieved from the message
    print "pose callback"
    print('x = {}'.format(pose_message.x))
    print('y = %f' %pose_message.y)
    print('yaw = {}'.format(pose_message.theta))

#moves robot to a specific spatial and angular coordinates 
def move(speed, distance):

    #declare a Twist message to send velocity commands
    velocity_message = Twist()
    
    #get current location from the global variable before entering the loop
    x0 = x
    y0 = y
    z0 = z
    yaw0 = yaw

    #assign the x-coordinate of linear velocity to the speed
    velocity_message.linear.x = speed
    distance_moved = 0.0

    #set rate of publishing 
    loop_rate = rospy.Rate(10) #we publish the velocity at 10 Hz (10 times a second)
    
    #What is this for..defning the topic???
    cmd_vel_topic = '/turtle1/cmd_vel'

    #create a publisher for the velocity message on the appropriate topic
    velocity_publisher = rospy.Publisher('location', Pose,  queue_size=10)
    rospy.init_node('talker', anonymous=True)

    while True : 
        rospy.loginfo("Turtlesim moves forwards")

        #publish the velocity message
        velocity_publisher.publish(velocity_message)
        
        #why do we need both of these?
        loop_rate.sleep()
        rospy.Duration(10)

        #measure the distance moved
        distance_moved = distance_moved + abs(0.5 * math.sqrt(((x-x0)**2)+((y-y0)**2)))
        print(distance_moved)
        if not(distance_moved < distance):
            rospy.loginfo("reached")
            break
        
    #publish a velocity message zero to make the robot stop after the distance is reached
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


if __name__== '__main__':
    try:

        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        #subscribe to the topic of the pose of the Turtlesim
        rospy.Subscriber("location", Pose, poseCallback) 

        #declare velocity publisher
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        #declare velocity subscriber
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)

        time.sleep(2)
        
        print 'move: '
        move(1.0, 5.0)
        time.sleep(2)
        print 'start reset: '
        rospy.wait_for_service('reset')
        reset_turtle = rospy.ServiceProxy('reset', Empty)
        reset_turtle()
        print 'end reset: '
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("node reminated.")
