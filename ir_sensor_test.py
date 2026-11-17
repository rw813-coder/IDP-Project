from machine import Pin, PWM
from time import sleep_ms

ir_sensorpin = 27
ir_sensor = Pin(ir_sensorpin, Pin.IN)          # digital output of IR sensor

RED_DETECTED = 1                     # change to 0 if your sensor is inverted
DRIVE_SPEED  = 45000                 # duty cycle, 0-65535



def sensor_value_test(): # binary value if light is red, traffic_light_value = 1 and vice versa
    value = ir_sensor.value()

    traffic_light_value = 1
    
    while True:


        if traffic_light_value == 1:
            sleep_ms(10)

        elif traffic_light_value == 0:
            sleep_ms(2000)

        
        traffic_light_value = 1

        if value != 1:
            trffic_light_value = 0


        print(traffic_light_value)


sensor_value_test()
