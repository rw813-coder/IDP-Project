from machine import Pin
from time import sleep
def run():
    buttonpin = ##
    ledpin = ##
    button = Pin(buttonpin,Pin.IN)
    led1 = Pin(ledpin,Pin.OUT)

    power = False
    if button.value() == 1:
        power = True
        print ("Power is on")
    while power == False:
        sleep(0.1)
    while power == True:
        led1.value(1)
        if button.value() == 0:
            power = False
            print ("Power is off")
            led1.value(0)
