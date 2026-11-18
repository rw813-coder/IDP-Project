from machine import Pin, PWM
from Servo import h_servo_pin, g_servo_pin
from movements import reverse, stop
import time


def box_grab():
    g_servo_pin.grab()

def box_release():
    g_servo_pin.open()

def grab_sequence():
    box_grab()
    h_servo_pin.set_height(height=5)
    timeout_ms = 2000
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        reverse()
    else:
        stop()
    
    