from motor import left_motor, right_motor
from initialization import led1
import time
def light_flash():
    while True:
        led1.value(1) 
        time.sleep(0.2)
        led1.value(0)
        time.sleep(0.2)
def forwards():
    light_flash()
    left_motor.normal_speed()
    right_motor.normal_speed()
    
def stop():
    left_motor.off()
    right_motor.off()

def veer(veerright = True):
    light_flash()
    if veerright:
        left_motor.normal_speed()
        right_motor.veer_speed()
    else:
        left_motor.veer_speed()
        right_motor.normal_speed()

def normal_drive(fr, fl):
    light_flash()
    'driving forwards with veering for correction'
    if fr.value() == 1 and fl.value() == 1:
        forwards()
    elif fr.value() == 0:
        veer(veerright = False)
    elif fl.value() == 0:
        veer()
    else: 
        stop()


def turn_90(rightturn, fr, fl):
    light_flash()
    if rightturn == True:
        while fl.value() == 0:
            left_motor.turn_speed()
            right_motor.off()
    else:
        while fr.value() == 0:
            left_motor.off()
            right_motor.turn_speed()
    stop()

def corner_turn(bl, br, fr, fl):
    light_flash()
    if bl == 0 and br == 0:
        forwards()
    else:
        turn_90(rightturn = (br == 1), fr = fr, fl = fl)


def depot_sequence(rightturn, fr, fl): 
    turn_90(rightturn=rightturn, fr =fr, fl=fl)
    while (fr.value() == 1) or (fl.value() == 1):
        normal_drive(fr = fr, fl = fl)
    if fr.value() and fl.value() == 0:
        time.sleep(3)
    return 1

def yard_sequence(rightturn, fr, fl):
    turn_90(rightturn = rightturn, fr = fr, fl = fl)
    while (fr.value() == 1) or (fl.value() == 1):
        normal_drive(fr = fr, fl = fl)
    else:
        return 1
        ## Drop off package
        ## Reverse
        ## Turn back the way you came
        ## Normal drive

