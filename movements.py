from motor import left_motor, right_motor
from hall_effect_sensor import determine_pole, package_present
import time
from initialization import check_stop_reset, wait_ms
from Servo import grab_servo, height_servo
from led import magnetic_field_light, light_turn_off


def forwards():
    left_motor.left_speed()
    right_motor.normal_speed()

def reverse():
    left_motor.reverse()
    right_motor.reverse()

def stop():
    left_motor.off()
    right_motor.off()

def forwards_time(timeout_ms, reversing = False):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        check_stop_reset()
        reverse() if reversing else forwards()
    else:
        stop()

def veer(veerright = True):
    if veerright:                      ### It HAS veered right, so need to reduce left motor speed
        left_motor.left_speed()
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
        wait_ms(40)         
    elif fr == 1 and fl == 0:          
        veer()
        wait_ms(40)
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

def leave_line(clockwise, fr, fl, timeout_ms = 3000):
    'Spin in place until neither front sensor sees the line'
    start = time.ticks_ms()
    while fr.value() or fl.value():
        check_stop_reset()
        spin(clockwise, True)
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            stop()
            return False
    stop()
    return True

def depot_drive(fr, fl, bl, br, reversing = False, rightturn = True):
    'Driving along the line for the depot/yard sequences'

    if not reversing:

        while True:
            check_stop_reset()
            rv, lv = fr.value(), fl.value()  
            if not rv and not lv:
                break
            correction(rv, lv)
    else:
        while True:
            check_stop_reset()
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            if brv and blv:
                break
            reverse_correction(rv, lv)
    stop()

def yard_drive(fr, fl, bl, br, reversing = False):
    'Driving along the line for the depot/yard sequences'
    if not reversing:
        while True:
            check_stop_reset()
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            if blv and brv:
                break
            correction(rv, lv)
    else:
        flag = 0
        while True:
            check_stop_reset()
            rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
            reverse_correction(rv, lv)
            if not brv and not blv and flag == 0:
                flag += 1
            elif (brv or blv) and flag == 1:
                flag += 1
            elif (not brv and not blv) and flag == 2:
                break
            else:
                continue
    stop()

def spin(clockwise, differential):
    if clockwise:
        left_motor.turn_speed()
        if differential: right_motor.reverse()
        else:     right_motor.off()
    else:
        right_motor.turn_speed()
        if differential: left_motor.reverse()
        else:       left_motor.off()

def rotate(clockwise, sensor, differential, timeout_ms, targets = (0, 1)):
    start = time.ticks_ms()
    for target in targets:        # 1st: leave the line, 2nd: find the next
        while sensor.value() != target:
            check_stop_reset()
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
        check_stop_reset()
        spin(clockwise, differential)
    else:
        stop()

def corrective_rotate(rightturn, fr, fl, timeout_ms = 5000, differential = False):
    'Turn until the front sensor on the side being turned towards reads 0'
    sensor = fr if rightturn else fl
    return rotate(rightturn, sensor, differential, timeout_ms, targets=(0,))

def turn_90(rightturn, fr, fl, timeout_ms = 5000, differential = False):
    '90 degree turn until front sensor not on the turning side goes to 1'
    return rotate(rightturn, fl if rightturn else fr, differential, timeout_ms)

def corner_turn(bl, br, fr, fl):
    '90 degree turns for corners - start turn when side sensor detects 1'
    if bl == 0 and br == 0:
        forwards()
    else:
        rightturn = br == 1
        turn_90(rightturn, fr = fr, fl = fl)
        return rightturn

def depot_sequence(rightturn, fr, fl, bl, br):
    'Turns into depot, picks up package, and exits depot'
    turn_90(rightturn, fr, fl)  #Turn into depot
    rotate_time(rightturn, True, 80)
    depot_drive(fr, fl, bl, br)
    forwards_time(50)         #Drive until line ends
    stop()
    grab_servo.grab()
    wait_ms(2000)
                                           #Stop to pick up package
                               
    depot_drive(fr, fl, bl, br, reversing = True)          #Reverse until the three-point junction
    turn_90(rightturn, fr, fl)               #Turn the same way as in entry to the depot


def yard_sequence(rightturn, fr, fl, bl, br):
    'Turns into yard, deposits package, and turns back to return to the start point'
    turn_90(rightturn, fr, fl)
    forwards_time(200)
    rotate_time(rightturn, True, 185)
    yard_drive(fr, fl, bl, br)
    stop()
    forwards_time(200, reversing = True)
    height_servo.lo()
    wait_ms(1000)                              #Stop to deposit package
    grab_servo.open()
    wait_ms(2000)
    height_servo.high()                              
    yard_drive(fr, fl, bl, br, reversing = True)
    leave_line(not rightturn, fr, fl)                                   # get off the yard line first
    turn_90(not rightturn, fr, fl, differential = False)            # then find the main line

def new_depot_sequence(rightturn, fr, fl, bl, br, entry = False, upper = False):
    'Turns into depot, picks up package, and exits depot'
    if entry:
        turn_90(rightturn, fr, fl, 5000, differential = True)  #Turn into depot
        forwards_time(600)
        rotate_time(rightturn, False, 500)
        forwards_time(350)
        rotate_time(rightturn, False, 100)
        # rotate_time(not rightturn, False, 100)
        # forwards_time(600)
    if upper:
        height_servo.lo()
    depot_drive(fr, fl, bl, br)         #Drive until line ends
    forwards_time(50)         #Drive forwards a little bit more
    stop()
    package_found = package_present()
    if package_found:
        grab_servo.grab()
        magnetic_field_light()
        wait_ms(1000)                             #Pick up the package
        if upper:
            height_servo.high()
        depot_drive(fr, fl, bl, br, reversing = True) #Reverse until the three-point junction
        if entry:
            turn_90(rightturn, fr, fl)           #Turn the opposite way as in entry to the depot
        else:
            turn_90(rightturn, fr, fl)
            turn_90(rightturn, fr, fl)
    else:                                                                                                                                    
        depot_drive(fr, fl, bl, br, reversing = True)    #Reverse until the three-point junction 
        turn_90(not rightturn, fr, fl)      #Turn the same way as in entry to the depot     
    return package_found    


def new_yard_sequence(rightturn, fr, fl, bl, br, change_dir):
    'Turns into yard, deposits package, and continues in same direction if change_dir is true'
    turn_90(rightturn, fr, fl)
    forwards_time(200)
    rotate_time(rightturn, True, 185)
    yard_drive(fr, fl, bl, br)
    stop()                             
    forwards_time(150, reversing = True)  #Reverse to get the package into the yard
    height_servo.lo()
    wait_ms(1000)
    grab_servo.open()                     #Deposit package
    light_turn_off()
    wait_ms(1000)
    height_servo.high()                           
    yard_drive(fr, fl, bl, br, reversing = True)
    leave_line(rightturn if change_dir else not rightturn, fr, fl)            # get off the yard line first
    turn_90(rightturn if change_dir else not rightturn, fr, fl, timeout_ms = 5000, differential = False)       # then find the main line

def junction_function(fr, fl , bl, br, upwards = False):
    flag = 0
    while True:
        check_stop_reset()
        blv, brv = bl.value(), br.value()
        normal_drive(fr, fl)                           
        if upwards:
            if flag == 0 and not brv and not blv:
                flag = 1
            elif flag == 1 and (brv or blv):
                wait_ms(25)                         #Can edit this value based on testing
                blv, brv = bl.value(), br.value()   #Re-read sensors after the sleep
                if blv and brv:
                    turn_90(determine_pole() == "north", fr, fl)
                else:
                    turn_90(brv == 1, fr, fl)
                    #### Read IR sensors here
                flag += 1                                 # now skip the four-point after the turn
            elif flag == 2 and blv and brv:
                flag += 1                                  # on the four-point
            elif flag == 3 and not blv and not brv:
                break      
        else:
            if not brv and not blv and flag == 0:
                flag += 1
            elif flag == 1 and brv and blv:
                flag += 1
            elif flag == 2 and not brv and not blv:
                break
    stop()


#### Needs editing completely
def upper_depots(fr, fl, bl, br, rightdirection = True):
    pos = 0
    package = False
    on_four_point = False            # True while still sitting on a four point already counted
    while True:
        check_stop_reset()
        blv, brv = bl.value(), br.value()
        new_four_point = bool(blv and brv)  #Triggers every time both of the rear sensors are 1

        if not new_four_point:
            on_four_point = False    # left the junction, so the next one counts as new

        if new_four_point and not on_four_point:
            on_four_point = True     # latch: handle each junction once

            if not package:
                if pos < 6:
                    package = new_depot_sequence(rightdirection, fr, fl, bl, br, entry = pos == 0, upper = True)
                    if not package:
                        pos += 1
                #### Exit sequence here
            else:
                pos -= 1           
                if pos < 0:      #This can be edited, but pos should be -1 at jnc
                    break
        normal_drive(fr, fl)       # reads the front sensors itself
                                   # Using normal_drive as it takes the pin objects (frontr etc) directly
    stop()
    return pos