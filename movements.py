from motor import left_motor, right_motor
from hall_effect_sensor import determine_pole
import time

def forwards():
    left_motor.normal_speed()
    right_motor.normal_speed()

def reverse():
    left_motor.reverse()
    right_motor.reverse()

def stop():
    left_motor.off()
    right_motor.off()

def forwards_time(timeout_ms):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        forwards()
    else:
        stop()

def veer(veerright = True):
    if veerright:                      ### It HAS veered right, so need to reduce left motor speed
        left_motor.normal_speed()
        right_motor.veer_speed()
    else:                              ### Vice versa
        left_motor.veer_speed()
        right_motor.normal_speed()

def reverse_veer(veerright = True):
    if veerright:
        left_motor.reverse_veer_speed()
        right_motor.reverse()
    else:
        left_motor.reverse()
        right_motor.reverse_veer_speed()

def correction(fr, fl):
    'driving forwards with veering for correction'
    if fr == 1 and fl == 1:
        forwards()
    elif fr == 0 and fl == 1:           
        veer(veerright = False)         
    elif fr == 1 and fl == 0:          
        veer()
    else: 
        stop()

def reverse_correction(fr, fl):
    if fr == 0 and fl == 1:           
        reverse_veer(veerright = False)         
    elif fr == 1 and fl == 0:          
        reverse_veer()
    else: 
        reverse()

def normal_drive(fr, fl):
    'using corrective driving (correction function) with constantly updating inputs'
    rv, lv = fr.value(), fl.value()
    correction(fr = rv, fl = lv)

def reverse_drive(fr, fl):
    rv, lv = fr.value(), fl.value()
    reverse_correction(fr = rv, fl = lv)

def depot_drive(fr, fl, bl, br, reversing = False):
    'Driving along the line for the depot/yard sequences'
    if not reversing:
        while True:
            rv, lv = fr.value(), fl.value()  
            if not rv and not lv:
                break
            correction(rv, lv)
    else:
        while True:
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            if brv and blv:
                break
            reverse_correction(rv, lv)
    stop()

def yard_drive(fr, fl, bl, br, reversing = False):
    'Driving along the line for the depot/yard sequences'
    if not reversing:
        while True:
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            if blv and brv:
                break
            correction(rv, lv)
    else:
        flag = 0
        while True:
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            reverse_correction(rv, lv)
            if not brv and not blv and flag == 0:
                flag += 1
            elif (brv and blv) and flag == 1:
                break
            else:
                continue
    stop()


def spin(clockwise, differential):
    if clockwise:
        left_motor.turn_speed()
        if differential: right_motor.reverse()
        else:        right_motor.off()
    else:
        right_motor.turn_speed()
        if differential: left_motor.reverse()
        else:        left_motor.off()

def rotate(clockwise, sensor, differential, timeout_ms):
    start = time.ticks_ms()
    for target in (0, 1):               # 1st: leave the line, 2nd: find the next
        while sensor.value() != target:
            spin(clockwise, differential)
            if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
                stop()
                return False            # gave up
    stop()
    return True

def rotate_time(clockwise, differential, timeout_ms):
    'Rotate for a fixed period of timeout ms, without a sensor-defined end state'
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        spin(clockwise, differential)
    else:
        stop()

def turn_90(rightturn, fr, fl, timeout_ms = 5000):
    '90 degree turn until front sensor not on the turning side goes to 1'
    return rotate(rightturn, fl if rightturn else fr, False, timeout_ms)

def corner_turn(bl, br, fr, fl):
    '90 degree turns for corners - start turn when side sensor detects 1'
    if bl == 0 and br == 0:
        forwards()
    else:
        turn_90(rightturn = (br == 1), fr = fr, fl = fl)

def depot_sequence(rightturn, fr, fl, bl, br):
    'Turns into depot, picks up package, and exits depot'
    turn_90(rightturn, fr, fl)  #Turn into depot
    depot_drive(fr, fl, bl, br)         #Drive until line ends
    stop()                              #Stop to pick up package
    time.sleep_ms(3000)                                   
    depot_drive(fr, fl, bl, br, reversing = True)          #Reverse until the three-point junction
    turn_90(rightturn, fr, fl)               #Turn the same way as in entry to the depot


def yard_sequence(rightturn, fr, fl, bl, br):
    'Turns into yard, deposits package, and turns back to return to the start point'
    turn_90(rightturn, fr, fl)
    forwards_time(200)
    rotate_time(rightturn, True, 185)
    yard_drive(fr, fl, bl, br)
    stop()                              #Stop to deposit package
    time.sleep_ms(3000)                               
    yard_drive(fr, fl, bl, br, reversing = True)
    if (rightturn and fl.value() == 1) or (not rightturn and fr.value()):
        turn_90(not rightturn, fr, fl)
    else:
        rotate_time(not rightturn, True, 150)
        turn_90(not rightturn, fr, fl)

