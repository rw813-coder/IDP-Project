from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep

def read_distance():
    #configure I2C Bus
    i2c_bus = I2C(id = 0, sda = Pin(20), scl = Pin(21)) # I2C0 on GP20 and 21

    #Setup vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0],18)
    vl53l0.set_VCsel_pulse_period(vl53l0.vcsel_period_type[1], 14)

    vl53l0.start()

    distance = vl53l0.read()

    vl53l0.stop()
    return distance

#It might be worth configuring I2C Bus and setting up vl53l0 object in main
#This function will do the set up every time it's called, which isn't ideal
#Then you could just use vl53l0.read() every time you need the distance instead of calling this function
#I didn't want to change main without checking first - Zac