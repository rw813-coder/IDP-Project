from Servo import grab_servo, height_servo
import time
def move_test_test():
    grab_servo.set_angle(270)


def grab_angle_test():

    for i in range(270):
        grab_servo.set_angle(i)
        time.sleep(0.1)
        print(i)

##grab_angle_test()
move_test_test()