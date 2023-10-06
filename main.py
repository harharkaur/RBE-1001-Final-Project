# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       harleen                                                      #
# 	Created:      10/5/2023, 11:41:04 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *
import time

#test1

brain = Brain()
left_motor = Motor(Ports.PORT1, True)
right_motor = Motor(Ports.PORT2)
arm_motor = Motor(Ports.PORT6)
RED_BALL = Signature (1, 7417, 8677, 8047, -879, -433, -656, 6.1, 0)
vision = Vision(Ports.PORT17, RED_BALL)


drive_speed = 50
turn_speed = 30
arm_speed = 20

camera_center_x = 155
camera_center_y = 105
camera_width = 310
camera_height = 210
center_x_threshold = 5
center_y_threshold = 50


while True:

    objects = vision.take_snapshot(RED_BALL)

    if objects:

        red_ball = vision.largest_object

        while abs(red_ball.centerX - camera_center_x) > center_x_threshold:
            error = red_ball.centerX - camera_center_x
            effort = (error * turn_speed) / camera_width
            left_motor.spin(REVERSE, effort, VelocityUnits.RPM)
            right_motor.spin(FORWARD, effort, VelocityUnits.RPM)
            time.sleep(0.1)
            vision.take_snapshot(RED_BALL)
            red_ball = vision.largest_object

        left_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)
        right_motor.spin(FORWARD, drive_speed, VelocityUnits.RPM)

        while (red_ball.centerY - camera_center_y) > center_y_threshold:
            time.sleep(0.25)
            vision.take_snapshot(RED_BALL)
            red_ball = vision.largest_object

        left_motor.stop()
        right_motor.stop()
        arm_motor.spin(FORWARD, arm_speed, VelocityUnits.RPM)
        time.sleep(1)
        arm_motor.stop()

    else:
        left_motor.spin(REVERSE, turn_speed, VelocityUnits.RPM)
        right_motor.spin(FORWARD, turn_speed, VelocityUnits.RPM)
        time.sleep(1)
        left_motor.stop()
        right_motor.stop()


        
