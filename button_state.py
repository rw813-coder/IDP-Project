from machine import Pin
from time import sleep_ms


def button_state(): #on is 1, off is 0

    button = Pin(22, Pin.IN)
    on = 0

    while True:

        
        if (on == 0) and (button.value() == 0):
            on = 1
            sleep_ms(750)

        elif (on == 1) and (button.value() == 0):
            on = 0
            sleep_ms(750)


button_state()