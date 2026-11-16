#import os
#print(os.listdir())      # what's really on the board
#import motor
#print(dir(motor))

from sensor_line import drive ###############, readings
from ir_sensor import sensor_value

print("Welcome to main.py!")
RED_DETECTED = 1
###readings()
drive()
RED_DETECTED = sensor_value()





