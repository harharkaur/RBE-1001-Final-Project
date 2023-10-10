# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       harleen                                                      #
# 	Created:      10/5/2023, 11:41:04 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Change test

# Library imports
import vex
import time

brain = vex.Brain()
left_motor = vex.Motor(vex.Ports.PORT1, True)
right_motor = vex.Motor(vex.Ports.PORT2)
arm_motor = vex.Motor(vex.Ports.PORT6)
pulley_motor = vex.Motor(vex.Ports.PORT10)
RED_BALL = vex.Signature (1, 7417, 8677, 8047, -879, -433, -656, 6.1, 0)
BLUE_BALL = vex.Signature(2, -2235, -1227, -1731, 6473, 9973, 8223, 3,0)
vision = vex.Vision(vex.Ports.PORT17, 50, RED_BALL, BLUE_BALL)


drive_speed = 70
turn_speed = 50
arm_speed = 20

camera_center_x = 155
camera_center_y = 105
camera_width = 310
camera_height = 210
center_x_threshold = 5
# center_y_threshold = 47

target_width = 35




while True:

    objects = vision.take_snapshot(BLUE_BALL)

    if objects:

        blue_ball = vision.largest_object()
        # width = blue_ball.width
        # print(width)

        while abs(blue_ball.centerX - camera_center_x) > center_x_threshold:
            error = blue_ball.centerX - camera_center_x
            effort = (error * turn_speed) / camera_width
            left_motor.spin(vex.FORWARD, effort, vex.VelocityUnits.RPM)
            right_motor.spin(vex.REVERSE, effort, vex.VelocityUnits.RPM)
            time.sleep(0.1)
            print("applied effort x")
            vision.take_snapshot(BLUE_BALL)
            blue_ball = vision.largest_object()

        left_motor.spin(vex.FORWARD, drive_speed, vex.VelocityUnits.RPM)
        right_motor.spin(vex.FORWARD, drive_speed, vex.VelocityUnits.RPM)

        while (blue_ball.width < target_width):
            time.sleep(0.25)
            print("drive closer")
            vision.take_snapshot(BLUE_BALL)
            blue_ball = vision.largest_object()

        left_motor.stop()
        right_motor.stop()
        arm_motor.spin(vex.REVERSE, arm_speed, vex.VelocityUnits.RPM)
        pulley_motor.spin(vex.FORWARD, 0.70, vex.VelocityUnits.RPM)
        time.sleep(5.2)
        print("arm moved")
        arm_motor.stop()
        pulley_motor.stop()

        time.sleep(5)

        left_motor.spin(vex.FORWARD, drive_speed, vex.VelocityUnits.RPM)
        right_motor.spin(vex.FORWARD, drive_speed, vex.VelocityUnits.RPM)

        time.sleep(5)

        left_motor.stop()
        right_motor.stop()

        arm_motor.spin(vex.FORWARD, arm_speed, vex.VelocityUnits.RPM)
        pulley_motor.spin(vex.REVERSE, 0.70, vex.VelocityUnits.RPM)
        time.sleep(5.2)
        print("arm moved up")
        arm_motor.stop()
        pulley_motor.stop()
        break

    else:
        left_motor.spin(vex.REVERSE, turn_speed, vex.VelocityUnits.RPM)
        right_motor.spin(vex.FORWARD, turn_speed, vex.VelocityUnits.RPM)
        time.sleep(1)
        print("obj not detected")
        left_motor.stop()
        right_motor.stop()
        
