from machine import Pin
from time import sleep


buttonpin = 15
ledpin = 16
button = Pin(buttonpin,Pin.IN)
led1 = Pin(ledpin,Pin.OUT)

bt = button.value()

power = False
if bt == 1:
    power = True
    print ("Power is on")
while power == False:
    sleep(0.1)
while power == True:
    led1 = 1
    if bt == 0:
        power = False
        print ("Power is off")
        led1.value(0)
