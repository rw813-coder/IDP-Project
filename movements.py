from global_data import wheelbase, wheeltrack
from motor import left_motor, right_motor

def forwards():
    left_motor.normal_speed()
    right_motor.normal_speed()

def stop():
    left_motor.off()
    right_motor.off()

def veer(veerright = True):
    if veerright:
        left_motor.normal_speed()
        right_motor.veer_speed()
    else:
        left_motor.veer_speed()
        right_motor.normal_speed()

def normal_drive(fr, fl):
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
    if bl == 0 and br == 0:
        forwards()
    else:
        turn_90(rightturn = (br == 1), fr = fr, fl = fl)


def depot_sequence(rightturn, fr, fl): 
    return 1

def yard_sequence(rightturn, fr, fl):
    turn_90(rightturn = rightturn, fr = fr, fl = fl)
    while (fr.value() == 1) or (fl.value() == 1):
        normal_drive(fr = fr, fl = fl)
    else:
        ## Drop off package
        ## Reverse
        ## Turn back the way you came
        ## Normal drive

