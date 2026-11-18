from machine import Pin, PWM
from time import sleep_ms

ir_sensorpin = 27
ir_sensor = Pin(ir_sensorpin, Pin.IN)          # digital output of IR sensor

DRIVE_SPEED  = 45000                 # duty cycle, 0-65535

def sensor_value(): # returns 1 when the light is green and the bot can go

    green = 0
    while True:

        if ir_sensor.value() == 0:
            green += 1
        
        sleep_ms(10)

        if green >= 10:
            break

    return 1