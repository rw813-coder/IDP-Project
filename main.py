#import os
#print(os.listdir())      # what's really on the board
#import motor
#print(dir(motor))

from sensor_line import drive
from sensor_line import readings

print("Welcome to main.py!")

readings()
drive()




