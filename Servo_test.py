from Servo import grab_servo, height_servo
import time

def grab_angle_test():

    for i in range(270):
        grab_servo.set_angle(i)
        time.sleep(0.1)
        print(i)

grab_angle_test()
    