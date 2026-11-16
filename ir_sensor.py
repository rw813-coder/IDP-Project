from machine import Pin, PWM
from time import sleep_ms
import numpy as np

ir_sensorpin = 27
ir_sensor = Pin(ir_sensorpin, Pin.IN)          # digital output of IR sensor

DRIVE_SPEED  = 45000                 # duty cycle, 0-65535

def sensor_value(traffic_light_value): # binary value if light is red, light = 1 and vice versa
    value = ir_sensor.value()

    while True:
        traffic_light_value = 1

        sleep_ms(1000)
        if value > 0.7:
            traffic_light_value = 1

        if value <= 0.7:
            confirm = []
            for i in range(50):
                confirm.append(value)
                sleep_ms(5)
            if np.average(confirm) <= 0.7:
                traffic_light_value = 0
        return traffic_light_value

def stop_car():
    motor_en.duty_u16(0)
    motor_in1.value(0)
    motor_in2.value(0)


def move_car():
    motor_in1.value(1)
    motor_in2.value(0)
    motor_en.duty_u16(DRIVE_SPEED)


def handle_traffic_light(ir_reading):
    """Takes the digital IR reading: red = stop, green = go."""
    if ir_reading == RED_DETECTED:
        stop_car()
    else:
        move_car()


stop_car()  # start safely stopped

while True:
    handle_traffic_light(ir_sensor.value())
    sleep_ms(50)