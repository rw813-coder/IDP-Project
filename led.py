from machine import Pin, Timer
import time
from motor import moving
from hall_effect_sensor import determine_pole

led1 = Pin(19, Pin.OUT) #yellow
led2 = Pin(18, Pin.OUT) #hgreen
led3 = Pin(17, Pin.OUT) #red

last_toggle = 0
led_on = 1

def update_led(timer):
    global last_toggle, led_on
    if moving():
        now = time.ticks_ms()
        if time.ticks_diff(now, last_toggle) >= 200:
            led_on = 1 - led_on
            led1.value(led_on)
            last_toggle = now
    else:
        led_on = 1
        led1.value(1)

_timer = Timer()
_timer.init(period=50, mode=Timer.PERIODIC, callback = update_led)

def light_turn_off(yellow_light_off = False):
    led2.value(0)
    led3.value(0)
    if yellow_light_off:
        led1.value(0)
    
def magnetic_field_light():
    if determine_pole == "north":
        led2.value(0)
        led3.value(1)
    elif determine_pole == "south":
        led2.value(1)
        led3.value(0)
    else:
        light_turn_off()


