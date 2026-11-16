from machine import Pin, PWM
from time import sleep_ms

ir_sensorpin = ##
ir_sensor = Pin(15, Pin.IN)          # digital output of IR sensor

RED_DETECTED = 1                     # change to 0 if your sensor is inverted
DRIVE_SPEED  = 45000                 # duty cycle, 0-65535


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