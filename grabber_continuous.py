from machine import Pin, Timer
import time
from 
from hall_effect_sensor import determine_pole
from Servo import grab_servo

def grab_cycle(timer):
    grab_servo.close()



_timer = Timer()
_timer.init(period=50, mode=Timer.PERIODIC, callback = grab_cycle())