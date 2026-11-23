from Servo import grab_servo, height_servo
import time
def move_test_test():
    grab_servo.set_angle(0)

def set_height():
    height_servo.set_angle(0)

def grab_angle_test():

    for i in range(270):
        grab_servo.set_angle(i)
        time.sleep(0.1)
        print(i)

def height_angle_test():

    for i in range(270):
        height_servo.set_angle(i)
        time.sleep(0.1)
        print(i)

set_height()