from machine import Pin
from time import sleep_ms



def on():
    on = 0
    button = Pin(22, Pin.OUT)
    button = 0


    while True:

        button = Pin(22, Pin.IN)

        print(button.value())

        if button.value() == 1:
            if on == 1:
                break

            else:
                on = 1

            button = Pin(22, Pin.OUT)
            button = 0

        print(on)


        