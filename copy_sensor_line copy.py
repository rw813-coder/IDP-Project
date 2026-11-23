from machine import Pin
from movements import stop, normal_drive, turn_90, corner_turn, new_yard_sequence, new_depot_sequence, upper_depots
import time
from initialization import button_pressed
from hall_effect_sensor import determine_pole

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
        normal_drive(frontr, frontl)


def delivery(location, in_pos, package_no, pole, YN, YS, correct_side = False):
    'Delivers the first and second packages, requires package = True and package_no to be 0 or 1'
    while True:
        fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
        three_point = is_three_point(fr, fl, bl, br)
        ### in_pos means need to switch sides, and then find depot, counting upwards
        if correct_side or in_pos:              
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
                if three_point:
                    skip_three_point()
                    location += 1 if correct_side else - 1   #correct_side only True when junction has been passed
                                    ##This happens when in_pos is false (needs to get to depot on other side, has passed jnc)
                                    ##Or when it has come from the upper depots
                elif not fr and not fl:
                        turned_right = corner_turn(bl, br, frontr, frontl)
                        if turned_right is not None:       # a turn actually happened    
                            location = 1 if correct_side else 0 #the else should not be called since in_pos being true means it delivers before
                                                                # the 90 degree turn
                else:
                    normal_drive(frontr, frontl)
        else:
        ### Needs to get past the junction, and then will be on the correct side
            if three_point and location == 0:         ### May need edit here
                junction_function()
                correct_side = True
            else:
                if three_point:
                    skip_three_point()
                    location -= 1
                elif not fr and not fl:
                    turned_right = corner_turn(bl, br, frontr, frontl)
                    if turned_right is not None:       # a turn actually happened    
                        location = 0
                else:
                    normal_drive(frontr, frontl)

def search_for_package(location, in_pos):
    'Searches for the first and second packages, requires package = False and package_no to be 0 or 1 to run'
    correct_side = in_pos
    while True:
        fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
        three_point = is_three_point(fr, fl, bl, br)
        if correct_side:
            if three_point and location == 3:
                depot_bay_checker()
                return 2
                #package = True after exiting, location set to 2
            else:
                if three_point:
                    skip_three_point()
                    location += 1
                elif not fr and not fl:
                    turned_right = corner_turn(bl, br, frontr, frontl)
                    if turned_right is not None:       # a turn actually happened    
                        location = 1
                else:
                    normal_drive(frontr, frontl)
        else:
            if three_point and location == 0:
                junction_function()
                correct_side = True
            else:
                if three_point:
                    skip_three_point()
                    location -= 1
                elif not fr and not fl:
                    turned_right = corner_turn(bl, br, frontr, frontl)
                    if turned_right is not None:       # a turn actually happened    
                        location = 0
                else:
                    normal_drive(frontr, frontl)

def junction_function(upwards = False):
    flag = 0
    while True:
        blv, brv = backl.value(), backr.value()
        normal_drive(frontr, frontl)                           
        if upwards:
            if flag == 0 and not brv and not blv:
                flag = 1
            elif flag == 1 and (brv or blv):
                time.sleep_ms(25)                         #Can edit this value based on testing
                blv, brv = backl.value(), backr.value()   #Re-read sensors after the sleep
                if blv and brv:
                    turn_90(determine_pole() == "north", frontr, frontl)
                else:
                    turn_90(brv == 1, frontr, frontl)
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


def depot_bay_checker():
    bay_no = 0
    while True:                                    # search outwards
        fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
        if (fr and fl and bl and not br) or (fr and fl and br and not bl):
            found = new_depot_sequence(br == 1, frontr, frontl, backl, backr)
            skip_three_point()
            if found:
                break
            bay_no += 1
        else:
            normal_drive(frontr, frontl)

    while bay_no > 0:                              # return past the empty bays
        fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
        if (fr and fl and bl and not br) or (fr and fl and br and not bl):
            skip_three_point()
            bay_no -= 1
        else:
            normal_drive(frontr, frontl)

def drive(): 
    global south, package, package_no, location, start, in_pos, YN, YS
 
    try:
        while True:

            if button_pressed():
                print("Power is off")
                break


            #Used to check and define the states (True/False)       
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
                if package_no < 2:       ### The first two packaged delivered, ends 
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
                        location = search_for_package(location, in_pos)
                        package = True

               ### The upper packages
                elif package_no in (2, 3):
                    if package:
                        pole = determine_pole()
                        junction_function(upwards = True)
                        location = 0
                        location = delivery(location, True, package_no, pole, YN, YS, correct_side = True)
                        ## in_pos always True for turn, correct_side is true to ensure locations counted up
                        package_no += 1
                        package = False
                        if pole == "south":
                            YS += 1
                        else:
                            YN += 1
                    else:
                        three_point = is_three_point(fr, fl, bl, br)
                        if three_point and location == 0:
                            junction_function(upwards = True)
                            upper_depots(frontr, frontl, backl, backr, True if package_no == 2 else False)  
                            #Should be generalised for sequential
                            package = True
                        else:
                            if three_point:
                                skip_three_point()
                                location -= 1
                            elif not fr and not fl:
                                turned_right = corner_turn(bl, br, frontr, frontl)
                                if turned_right is not None:       # a turn actually happened    
                                    location = 0
                            else:
                                normal_drive(frontr, frontl)

                ##Exit sequence, drive to junction and stop
                else:
                    three_point = is_three_point(fr, fl, bl, br)
                    if three_point and location == -1:         
                        stop() 
                        break
                    else:
                        if three_point:
                            skip_three_point()
                            location -= 1
                        elif not fr and not fl:
                            turned_right = corner_turn(bl, br, frontr, frontl)
                            if turned_right is not None:       # a turn actually happened    
                                location = 0
                        else:
                            normal_drive(frontr, frontl)


    finally:
        stop()
    
def reset_state():
    global location, package, package_no, in_pos, start, YN, YS
    package = False
    location = 0
    package_no = 0
    in_pos = True
    start = True
    YN, YS = 0, 0

def main(reset = False):
    while True:
        print("Waiting for button")
        while not button_pressed():
            time.sleep_ms(20)
        print("Power is on")
        if reset:
            reset_state()
        drive()               # returns when the button is pressed again

if __name__ == "__main__":
    main()


