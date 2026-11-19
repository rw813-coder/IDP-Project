from machine import Pin, PWM
from Servo import height_servo, grab_servo
from movements import reverse, stop
import time


def box_grab():
    grab_servo.grab()

def box_release():
    grab_servo.open()

def grab_sequence():
    box_grab()
    height_servo.set_height(height=30)
    timeout_ms = 2000
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        reverse()
    else:
        stop()

def drop_sequence():
    height_servo.set_height(height=10)
    box_release()
    
    
    