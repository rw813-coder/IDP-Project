from Servo import h_servo_pin, g_servo_pin
import time

def grab_angle_test():

    for i in range(270):
        g_servo_pin.set_angle(i)
        time.sleep(0.1)
        print(i)

grab_angle_test()
    