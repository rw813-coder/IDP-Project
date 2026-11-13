from machine import Pin
import time
from motor import moving

led1 = Pin(16, Pin.OUT)
last_toggle = 0
led_on = 0

def light_flash():
    global last_toggle, led_on
    if not moving():
        led_on = 0
        led1.value(0)
        return
    now = time.ticks_ms()
    if time.ticks_diff(now, last_toggle) >= 200:
        led_on = 1 - led_on
        led1.value(led_on)
        last_toggle = now