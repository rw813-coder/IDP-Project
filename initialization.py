from machine import Pin
import time
from motor import left_motor, right_motor

button = Pin(22, Pin.IN, Pin.PULL_DOWN)

last_state = button.value()
last_time = 0

def button_pressed():
    'True once per press (rising edge, debounced)'
    global last_state, last_time
    state = button.value()
    now = time.ticks_ms()
    pressed = (state == 1 and last_state == 0
               and time.ticks_diff(now, last_time) > 750)
    if pressed:
        last_time = now
    last_state = state
    return pressed

def stop():
    left_motor.off()
    right_motor.off()

class Stop(Exception):
    pass

def check_stop_reset():
    if button_pressed():
        raise Stop

def wait_ms(ms):
    'Interruptible replacement for time.sleep_ms'
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < ms:
        check_stop_reset()
        time.sleep_ms(5)