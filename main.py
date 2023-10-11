# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       harleen                                                      #
# 	Created:      10/9/2023, 5:26:58 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import time



brain = Brain()
left_motor = Motor(Ports.PORT1, True)
right_motor = Motor(Ports.PORT2)
arm_motor = Motor(Ports.PORT6)
pulley_motor = Motor(Ports.PORT10)
RED_BALL = Signature (1, 7417, 8677, 8047, -879, -433, -656, 6.1, 0)
BLUE_BALL = Signature(2, -2235, -1227, -1731, 6473, 9973, 8223, 3,0)
GREEN_SQUARE = Signature(3, -4579, -4469, -4524, -3673, -3291, -3482, 3,0)
vision = Vision(Ports.PORT17, 50, RED_BALL, BLUE_BALL, GREEN_SQUARE)
inertial = Inertial(Ports.PORT20)
ultrasonic_front = Sonar(brain.three_wire_port.a)
ultrasonic_side = Sonar(brain.three_wire_port.c)


drive_speed = 90
turn_speed = 60
arm_speed = 20

camera_center_x = 155
camera_center_y = 105
camera_width = 310
camera_height = 210
center_x_threshold = 5
# center_y_threshold = 47

target_width = 35

def ball_finder():
    
    blue_ball = vision.largest_object()

    while abs(blue_ball.centerX - camera_center_x) > center_x_threshold:
        error = blue_ball.centerX - camera_center_x
        effort = (error * turn_speed) / camera_width
        left_motor.spin(FORWARD, effort, VelocityUnits.RPM)
        right_motor.spin(REVERSE, effort, VelocityUnits.RPM)
        time.sleep(0.1)
        print("applied effort x")
        vision.take_snapshot(BLUE_BALL)
        blue_ball = vision.largest_object()

    left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
    right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)

    while (blue_ball.width < target_width):
        time.sleep(0.25)
        print("drive closer")
        vision.take_snapshot(BLUE_BALL)
        blue_ball = vision.largest_object()

    left_motor.stop()
    right_motor.stop()
    arm_motor.spin(REVERSE, arm_speed, VelocityUnits.RPM)
    pulley_motor.spin(FORWARD, 1, VelocityUnits.RPM)
    time.sleep(5.2)
    print("arm moved")
    arm_motor.stop()
    pulley_motor.stop()

    time.sleep(5)

    left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
    right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)

    time.sleep(3)

    left_motor.stop()
    right_motor.stop()

    arm_motor.spin(FORWARD, arm_speed, VelocityUnits.RPM)
    pulley_motor.spin(REVERSE, 1, VelocityUnits.RPM)
    time.sleep(5.2)
    print("arm moved up")
    arm_motor.stop()
    pulley_motor.stop()


def ball_delivery():

    green = vision.take_snapshot(GREEN_SQUARE)
    print ("green snapshot")

    if green:

        green_square = vision.largest_object()

        while abs(green_square.centerX - camera_center_x) > center_x_threshold:
            error = green_square.centerX - camera_center_x
            effort = (error * turn_speed) / camera_width
            left_motor.spin(FORWARD, effort, VelocityUnits.RPM)
            right_motor.spin(REVERSE, effort, VelocityUnits.RPM)
            time.sleep(0.1)
            print("applied effort x")
            vision.take_snapshot(GREEN_SQUARE)
            green_square = vision.largest_object()

        ultrasonic_front_distance = ultrasonic_front.distance(MM)
        
        while (ultrasonic_front_distance > 50):
            left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
            right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
            ultrasonic_front_distance = ultrasonic_front.distance(MM)
            
        left_motor.stop()
        right_motor.stop()

    else:
        left_motor.spin(REVERSE, turn_speed, VelocityUnits.RPM)
        right_motor.spin(FORWARD, turn_speed, VelocityUnits.RPM)
        wait(1000)
        print("obj not detected")
        left_motor.stop()
        right_motor.stop()
        ball_delivery()

## gyroscope - set to 0 in front of ramp 
inertial.calibrate()
time.sleep(2)
print(inertial.heading())
heading = inertial.heading()

## spin 90 and look for ball 

while (heading < 100) or (heading > 200):
    left_motor.spin(FORWARD, turn_speed)
    right_motor.spin(REVERSE, turn_speed)
    print(inertial.heading())
    heading = inertial.heading()
    wait(10)

left_motor.stop()
right_motor.stop()
wait(1000)
objects = vision.take_snapshot(BLUE_BALL)
print("snapshot 1 taken")
if objects:
    ## go for ball and deliver ball loop
    ball_finder()
    print("completed ball finder")
    ball_delivery()
    print("ball delivered")
    
## if no ball detected, spin 180 and look for ball

else:
    while heading < 300:
        left_motor.spin(FORWARD, turn_speed)
        right_motor.spin(REVERSE, turn_speed)
        print(inertial.heading())
        heading = inertial.heading()
        wait(10)

    left_motor.stop()
    right_motor.stop()
    objects = vision.take_snapshot(BLUE_BALL)
    ## go for ball and deliver ball loop
    ball_finder()
    print("completed ball finder")
    ball_delivery()
    print("ball delivered")


## begin lap around feild and identify another ball 
## ball loop 
## counter = 2 for all balls collected 
## when counter = 2; turn 180 and drive back to certain distance from back wall 
## identifies left or right location by side ultrasonic sensor 
## turns according to ultrasonic distance from side sensor 
## drive forward until front ultrasonic sensor detect midpoint distance 
## turns to heading = 0 
## drives up ramp maintating heading =0 and pitch to modify velocity 
## dead reakon time to go up ramp 




# while True:

#     objects = vision.take_snapshot(BLUE_BALL)
    

#     if objects:

#         blue_ball = vision.largest_object()
#         # width = blue_ball.width
#         # print(width)

#         while abs(blue_ball.centerX - camera_center_x) > center_x_threshold:
#             error = blue_ball.centerX - camera_center_x
#             effort = (error * turn_speed) / camera_width
#             left_motor.spin(FORWARD, effort, VelocityUnits.RPM)
#             right_motor.spin(REVERSE, effort, VelocityUnits.RPM)
#             time.sleep(0.1)
#             print("applied effort x")
#             vision.take_snapshot(BLUE_BALL)
#             blue_ball = vision.largest_object()

#         left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#         right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)

#         while (blue_ball.width < target_width):
#             time.sleep(0.25)
#             print("drive closer")
#             vision.take_snapshot(BLUE_BALL)
#             blue_ball = vision.largest_object()

#         left_motor.stop()
#         right_motor.stop()
#         arm_motor.spin(REVERSE, arm_speed, VelocityUnits.RPM)
#         pulley_motor.spin(FORWARD, 0.70, VelocityUnits.RPM)
#         time.sleep(5.2)
#         print("arm moved")
#         arm_motor.stop()
#         pulley_motor.stop()

#         time.sleep(5)

#         left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#         right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)

#         time.sleep(5)

#         left_motor.stop()
#         right_motor.stop()

#         arm_motor.spin(FORWARD, arm_speed, VelocityUnits.RPM)
#         pulley_motor.spin(REVERSE, 0.70, VelocityUnits.RPM)
#         time.sleep(5.2)
#         print("arm moved up")
#         arm_motor.stop()
#         pulley_motor.stop()
#         break

#     else:
#         left_motor.spin(REVERSE, turn_speed, VelocityUnits.RPM)
#         right_motor.spin(FORWARD, turn_speed, VelocityUnits.RPM)
#         time.sleep(1)
#         print("obj not detected")
#         left_motor.stop()
#         right_motor.stop()
        





## gyroscope - set to 0 in front of ramp 
## spin until spot ball 
## go for ball and deliver ball loop 
## begin lap around feild and identify another ball 
## ball loop 
## counter = 2 for all balls collected 
## when counter = 2; turn 180 and drive back to certain distance from back wall 
## identifies left or right location by side ultrasonic sensor 
## turns according to ultrasonic distance from side sensor 
## drive forward until front ultrasonic sensor detect midpoint distance 
## turns to heading = 0 
## drives up ramp maintating heading =0 and pitch to modify velocity 
## dead reakon time to go up ramp 

# line_follower_center = Line(brain.three_wire_port.f) 
# line_follower_left = Line(brain.three_wire_port.g)
# line_follower_right = Line(brain.three_wire_port.h)

# # Set the threshold value
# threshold = 750

# # Wait for 2 seconds
# time.sleep(2)

# # Main loop
# while True:

#     center_sensor_value = line_follower_center.value()
#     left_sensor_value = line_follower_left.value()
#     right_sensor_value = line_follower_right.value()

#     while (((right_sensor_value > threshold) or (left_sensor_value > threshold)) and (center_sensor_value < threshold)):
#         # Read line follower sensor values

#         center_sensor_value = line_follower_center.value()
#         left_sensor_value = line_follower_left.value()
#         right_sensor_value = line_follower_right.value()
#         print("right sensor", right_sensor_value)
#         print("center", center_sensor_value)
#         Kp = 0.1

#         difference = left_sensor_value - right_sensor_value
#         effort = difference * Kp
    
#         left_speed = drive_speed - effort
#         right_speed = drive_speed + effort

#         left_motor.spin(FORWARD, left_speed)
#         right_motor.spin(FORWARD, right_speed)
    


#     if (right_sensor_value < threshold) and (left_sensor_value < threshold) and (center_sensor_value < threshold):
#         # Spin 90 degrees
#         left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#         right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#         time.sleep(2)
#         left_motor.stop()
#         right_motor.stop()
#         left_motor.spin_to_position(90, RotationUnits.DEG, drive_speed, VelocityUnits.PERCENT, False)
#         right_motor.spin_to_position(90, RotationUnits.DEG, drive_speed, VelocityUnits.PERCENT, True)
#         left_motor.stop()
#         right_motor.stop()
#         left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#         right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#         time.sleep(2)
#         left_motor.stop()
#         right_motor.stop()

#     # Display sensor values (optional)
#     # print(f"Left: {left_sensor_value}  Center: {center_sensor_value}  Right: {right_sensor_value}")
    

#     # # RIGHT sensor sees light:
#     # if (right_sensor_value < threshold) and (left_sensor_value < threshold) and (center_sensor_value < threshold):
#     #     # # Spin 90 degrees
#     #     # left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#     #     # right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#     #     # time.sleep(2)
#     #     left_motor.stop()
#     #     right_motor.stop()
#     #     # left_motor.spin_to_position(90, RotationUnits.DEG, 63, VelocityUnits.PERCENT, False)
#     #     # right_motor.spin_to_position(-90, RotationUnits.DEG, 63, VelocityUnits.PERCENT, True)
#     #     # left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#     #     # right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
#     #     # time.sleep(2)
#     #     # left_motor.stop()
#     #     # right_motor.stop()
#     # elif right_sensor_value < threshold:
#     #     # Counter-steer right
#     #     left_motor.spin(FORWARD, drive_speed)
#     #     right_motor.spin(FORWARD, 40)
#     # # LEFT sensor sees light:
#     # elif left_sensor_value < threshold:
#     #     # Counter-steer left
#     #     left_motor.spin(FORWARD, 40)
#     #     right_motor.spin(FORWARD, drive_speed)
#     # else:
#     #     # CENTER sensor sees light and goes forward 
#     #     left_motor.spin(FORWARD, drive_speed)
#     #     right_motor.spin(FORWARD, drive_speed)
 