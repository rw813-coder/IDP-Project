from motor import left_motor, right_motor, moving
import time
from led import light_flash, led1


def forwards():
    left_motor.normal_speed()
    right_motor.normal_speed()

def reverse():
    left_motor.reverse()
    right_motor.reverse()

def stop():
    left_motor.off()
    right_motor.off()
    led1.value(0)

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
            light_flash()
    else:
        while True:
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            if brv and blv:
                break
            reverse_correction(rv, lv)
            light_flash()
    stop()

def yard_drive(fr, fl, bl, br, reversing = False):
    'Driving along the line for the depot/yard sequences'
    if not reversing:
        while True:
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            if blv and brv:
                break
            correction(rv, lv)
            light_flash()
    else:
        flag = 0
        while True:
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            reverse_correction(rv, lv)
            light_flash()
            if not brv and not blv and flag == 0:
                flag += 1
            elif (brv or blv) and flag == 1:
                flag += 1
            elif (brv or blv) and flag == 2:
                flag += 1
            elif not brv and not blv and flag == 3:
                break
            reverse_correction(rv, lv)
            light_flash()
    stop()


def spin(clockwise, in_place):
    if clockwise:
        left_motor.turn_speed()
        if in_place: right_motor.reverse()
        else:        right_motor.off()
    else:
        right_motor.turn_speed()
        if in_place: left_motor.reverse()
        else:        left_motor.off()

def rotate(clockwise, sensor, in_place, timeout_ms):
    start = time.ticks_ms()
    for target in (0, 1):               # 1st: leave the line, 2nd: find the next
        while sensor.value() != target:
            spin(clockwise, in_place)
            light_flash()
            if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
                stop()
                return False            # gave up
    stop()
    return True

def turn_90(rightturn, fr, fl, timeout_ms = 5000):
    return rotate(rightturn, fl if rightturn else fr, False, timeout_ms)

def corner_turn(bl, br, fr, fl):
    light_flash()
    if bl == 0 and br == 0:
        forwards()
    else:
        turn_90(rightturn = (br == 1), fr = fr, fl = fl)

def depot_sequence(rightturn, fr, fl, bl, br):
    turn_90(rightturn, fr, fl)  #Turn into depot
    depot_drive(fr, fl, bl, br)         #Drive until line ends
    end = time.ticks_add(time.ticks_ms(), int(3000))    #Pick up package
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        light_flash()                                       
    depot_drive(fr, fl, bl, br, reversing = True)          #Reverse until the three-point junction
    turn_90(rightturn, fr, fl)               #Turn the same way as in entry to the depot


def yard_sequence(rightturn, fr, fl, bl, br):
    turn_90(rightturn, fr, fl)
    yard_drive(fr, fl, bl, br)
    end = time.ticks_add(time.ticks_ms(), int(3000))       #Deposit package
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        light_flash()                             
    yard_drive(fr, fl, bl, br, reversing = True)
    turn_90(not rightturn, fr, fl) 

