from Servo import grab_servo, height_servo
import time
def closed_teeth():
    grab_servo.set_angle(270)

def open_teeth():
    grab_servo.set_angle(180)

def set_height():
    height_servo.set_angle(75)

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

open_teeth()
#closed_teeth()