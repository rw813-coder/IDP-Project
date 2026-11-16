from machine import Pin
import time

button = Pin(15, Pin.IN)

last_state = 0
last_time = 0

def button_pressed():
    'True once per press (rising edge, debounced)'
    global last_state, last_time
    state = button.value()
    now = time.ticks_ms()
    pressed = (state == 1 and last_state == 0
               and time.ticks_diff(now, _last_time) > 250)
    if pressed:
        last_time = now
    last_state = state
    return pressed
