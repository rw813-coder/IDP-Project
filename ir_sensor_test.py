from machine import Pin, PWM
from time import sleep_ms

ir_sensorpin = 27
ir_sensor = Pin(ir_sensorpin, Pin.IN)          # digital output of IR sensor

RED_DETECTED = 1                     # change to 0 if your sensor is inverted
DRIVE_SPEED  = 45000                 # duty cycle, 0-65535

while True:
    print(ir_sensor.value())
    sleep_ms(500)

""" def sensor_value_test(): # binary value if light is red, light = 1 and vice versa
    value = ir_sensor.value()

    while True:

        sleep_ms(1000)

        traffic_light_value = 1

        if value > 0.7:
            traffic_light_value = 1

        if value <= 0.7:
            confirm = []
            for i in range(50):
                confirm.append(value)
                sleep_ms(5)
                
            sum = 0
            
            for value in confirm:
                sum += value
                
            length = len(confirm)
            
            average = sum / length
                
            if average <= 0.7:
                traffic_light_value = 0

        print(traffic_light_value) """


sensor_value_test()
