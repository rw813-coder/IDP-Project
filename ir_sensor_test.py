from machine import Pin, PWM
from time import sleep_ms

ir_sensorpin = 27
ir_sensor = Pin(ir_sensorpin, Pin.IN)          # digital output of IR sensor

RED_DETECTED = 1                     # change to 0 if your sensor is inverted
DRIVE_SPEED  = 45000                 # duty cycle, 0-65535



def sensor_value_test(): # if 1 then go
    value = ir_sensor.value()

    go = 0
    
    while True:

        print(value)

        if value == 0:
            go = 1
            print(go)
            break

        sleep_ms(5)

sensor_value_test()

