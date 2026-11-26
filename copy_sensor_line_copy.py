from machine import Pin
from movements import stop, normal_drive, corner_turn, new_yard_sequence, new_depot_sequence, upper_depots, junction_function
import time
from initialization import button_pressed, check_stop_reset, Stop
from hall_effect_sensor import determine_pole
from Servo import grab_servo, height_servo
from led import light_turn_off

sens1 = 8
sens2 = 9 
sens3 = 10
sens4 = 11

#Pin objects
frontr = Pin(sens1, Pin.IN)  ##Front right
frontl = Pin(sens2, Pin.IN)  ##Front left
backl = Pin(sens3, Pin.IN)  ##Back left
backr = Pin(sens4, Pin.IN)  ##Back right

package = False
south = True    ### The initial direction, which is determined in the start up sequence, where south is the right hand side
package_no = 0
location = 0
in_pos = True
YN, YS = 0, 0

start = True

def is_three_point(fr, fl, bl, br):
    return (fr and fl and bl and not br) or (fr and fl and br and not bl)

def skip_three_point():
    while backl.value() or backr.value():
        check_stop_reset()
        normal_drive(frontr, frontl)

def location_update(location, fr, fl, bl, br, three_step, corner):
    '''One driving step. Updates location if at a three_point or corner. Three step dictates whether
    locations are incrementing or decrementing, and corner sets it at 1 or 0 after corner turn'''
    check_stop_reset()
    if is_three_point(fr, fl, bl, br):
        skip_three_point()
        return location + three_step
    elif not fr and not fl:
        if corner_turn(bl, br, frontr, frontl) is not None:
            return corner
    else:
        normal_drive(frontr, frontl)
    return location


def delivery(location, in_pos, package_no, pole, YN, YS, correct_side = False):
    'Delivers the first and second packages, requires package = True and package_no to be 0 or 1'
    while True:
        check_stop_reset()
        fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
        three_point = is_three_point(fr, fl, bl, br)
        ### in_pos means need to switch sides, and then find depot, counting upwards
        if correct_side or not in_pos:              
        ### If correct side, it has already passed the junction, location will become 1 once corner_turn is executed
        ## If in_pos, it doesn't need junction, but location counts down from 3 to 2 or 1.
            target = YN + 1 if pole == "north" else YS + 1
            if three_point and location == target:
                if package_no == 0:
                    new_yard_sequence(br == 1, frontr, frontl, backl, backr, change_dir = False) 
                    ##Always continues the way it came to get to the second depot
                else:
                    new_yard_sequence(br == 1, frontr, frontl, backl, backr, change_dir = in_pos)
                    ##If in_pos is False, it has come from the same depot, so needs to continue straight to get to jnc
                    ##Else it will turn around, going the way it came, to go to the junction
                return location
                #Package no += 1, package = False, and redefines in_pos after exiting
            else:
                location = location_update(location, fr, fl, bl, br, 1 if correct_side else -1,
                                           1 if correct_side else 0)    ### The 0 here should not be used
        else:
        ### Needs to get past the junction, and then will be on the correct side
            if three_point and location == 0:         ### May need edit here
                junction_function(frontr, frontl, backl, backr)
                correct_side = True
            else:
                location = location_update(location, fr, fl, bl, br, -1, 0)

def search_for_package(location, in_pos):
    'Searches for the first and second packages, requires package = False and package_no to be 0 or 1 to run'
    correct_side = in_pos
    while True:
        check_stop_reset()
        fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
        three_point = is_three_point(fr, fl, bl, br)
        if correct_side:
            if three_point and location == 3:
                depot_bay_checker(br == 1)
                return 2
                #package = True after exiting, location set to 2
            else:
                location = location_update(location, fr, fl, bl, br, 1, 1)
        else:
            if three_point and location == 0:
                junction_function(frontr, frontl, backl, backr)
                correct_side = True
            else:
                location = location_update(location, fr, fl, bl, br, -1, 0)

def depot_bay_checker(rightturn):
    'Checks all the bays in the depot until package is found'
    bay_no = 0
    while True:
        found = new_depot_sequence(rightturn, frontr, frontl, backl, backr, bay_no == 0)
        if found or bay_no == 5:              # 6 bays: 0 to 5
            break
        bay_no += 1
    skip_three_point() 

    while bay_no > 0:                         # return past the empty bays
        check_stop_reset()
        fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
        if is_three_point(fr, fl, bl, br):
            skip_three_point()
            bay_no -= 1
        else:
            normal_drive(frontr, frontl)

def drive(): 
    global south, package, package_no, location, start, in_pos, YN, YS
 
    try:
        while True:

            check_stop_reset()

            #Used to check and define the states (True/False) - Booleans, not pins 
            fr = frontr.value()
            fl = frontl.value()
            bl = backl.value()
            br = backr.value()

            ### Start sequence, exits with the first turn
            if start == True:
                if not fr and not fl:
                    turned_right = corner_turn(bl, br, frontr, frontl) # Initial right turn -  heading north
                    if turned_right is not None:       # a turn actually happened
                        south = not turned_right           
                        start = False
                        location = 1
                else:
                    normal_drive(frontr, frontl)

            else:
                if package_no < 1:       ### The first two packaged delivered, ends 
                    if package:
                        pole = determine_pole()
                        in_pos = south and pole == "north" or not south and pole == "south"
                        ###if in_pos, needs to switch sides, else stay on same side
                        location = delivery(location, in_pos, package_no, pole, YN, YS)
                        package_no += 1
                        package = False
                        if pole == "south":
                            YS += 1
                        else:
                            YN += 1
                        if in_pos:
                            south = not south 
                            #### Required to switch the side, if in_pos is now true it means it switched sides, and if
                            #### in_pos is false it means it is still on the same side
                    else:
                        location = search_for_package(location, in_pos) #in_pos only important for package_no = 1, True for 0
                        package = True

               ### The upper packages
                # elif package_no in (2, 3):
                #     if package:
                #         pole = determine_pole()
                #         junction_function(frontr, frontl, backl, backr, upwards = True)
                #         location = 0
                #         location = delivery(location, True, package_no, pole, YN, YS, correct_side = True)
                #         ## in_pos always True for turn, correct_side is true to ensure locations counted up
                #         package_no += 1
                #         package = False
                #         if pole == "south":
                #             YS += 1
                #         else:
                #             YN += 1
                #     else:
                #         three_point = is_three_point(fr, fl, bl, br)
                #         if three_point and location == 0:
                #             junction_function(frontr, frontl, backl, backr, upwards = True)
                #             upper_depots(frontr, frontl, backl, backr, True if package_no == 2 else False)  
                #             #Should be generalised for sequential
                #             package = True
                #         else:
                #             location = location_update(location, fr, fl, bl, br, -1, 0)

                ##Exit sequence, drive to junction and stop
                else:
                    three_point = is_three_point(fr, fl, bl, br)
                    if three_point and location == -1:         
                        stop() 
                        break
                    else:
                        location = location_update(location, fr, fl, bl, br, -1, 0)

    except Stop:
        print("Button stop; press button again to restart")
    finally:
        stop()
        reset_state()
    
def reset_state():
    global location, package, package_no, in_pos, start, YN, YS
    package = False
    location = 0
    package_no = 0
    in_pos = True
    start = True
    YN, YS = 0, 0
    grab_servo.open()
    height_servo.high()
    light_turn_off()

def main():
    while True:
        print("Waiting for button")
        while not button_pressed():
            time.sleep_ms(20)
        print("Power is on")
        drive()               # returns when the button is pressed again

if __name__ == "__main__":
    main()


