from machine import Pin
from movements import stop, normal_drive, corner_turn, yard_sequence, new_yard_sequence, new_depot_sequence, junction_function, upper_depots
import time
from initialization import button_pressed
from hall_effect_sensor import determine_pole

##north poles need to go to the left


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
location = 1
in_pos = True
increment = False
YN, YS = 0, 0


def skip_three_point():
    while backl.value() or backr.value():
        normal_drive(frontr, frontl)

def depot_bay_checker():
    'sequentially checks the bays for a package, and exits when a package has been found and the vehicle has exited the bays'
    fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
    three_point = three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)
    bay_no = 0
    package_found = False
    while not package_found:
        if three_point:
            package_found = new_depot_sequence(rightturn = (br == 1), fr = frontr, fl = frontl, bl = backl, br = backr)
            bay_no += 1
        else:
            normal_drive(frontr, frontl)
    else:
        if three_point and bay_no == 0:
            skip_three_point()
            break
        elif three_point and bay_no > 0:
            skip_three_point()
            bay_no -= 1
        else:
            normal_drive(frontr, frontl)

def delivery(location, in_pos, package_no, pole, YN, YS):
    'Delivers the first and second packages, requires package = True and package_no to be 0 or 1'
    fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
    correct_side = in_pos
    three_point = three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)
    if correct_side:
        target = YN + 1 if pole == "north" else YS + 1
        if three_point and location == target:
            if package_no == 0:
                new_yard_sequence(br == 1, fr, fl, bl, br, in_pos)
            else:
                yard_sequence(br == 1, fr, fl, bl, br)
            break
            #Package no += 1, package = False, and redefines in_pos after exiting
        else:
            if three_point:
                skip_three_point()
                location += 1
            elif not fr and not fl:
                corner_turn(bl, br, frontr, frontl)
                location = 1
            else:
                normal_drive(frontr, frontl)
    else:
        if three_point and location == 0:
            junction_function(frontr, frontl, backl, backr)
            correct_side = True
        else:
            if three_point:
                skip_three_point()
                location -= 1
            elif not fr and not fl:
                corner_turn(bl, br, frontr, frontl)
                location = 1
            else:
                normal_drive(frontr, frontl)


def search_for_package(frontr, frontl, backl, backr, location, in_pos):
    'Searches for the first and second packages, requires package = False and package_no to be 0 or 1 to run'
    fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
    correct_side = in_pos
    three_point = three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)
    if correct_side:
        if three_point and location == 3:
            depot_bay_checker(br == 1, frontr, frontl, backl, backr)
            break
            #package = True after exiting, location set to 3
        else:
            if three_point:
                skip_three_point()
                location += 1
            elif not fr and not fl:
                corner_turn(bl, br, frontr, frontl)
            else:
                normal_drive(frontr, frontl)
    else:
        if three_point and location == 0:
            junction_function(frontr, frontl, backl, backr)
            correct_side = True
        else:
            if three_point:
                skip_three_point()
                location += 1
            elif not fr and not fl:
                corner_turn(bl, br, frontr, frontl)
            else:
                normal_drive(frontr, frontl)


def drive(): 
    global package, package_no, right, location, increment, start, in_pos, YN, YS
 
    try:
        while True:

            start = True
            if button_pressed():
                print("Power is off")
                break

            #Used to check and define the states (True/False)       
            fr = frontr.value()
            fl = frontl.value()
            bl = backl.value()
            br = backr.value()

            ### All three point states dealt with first; 
            ### Depot and yard, with events taken chronologically (for now)
            ###
            three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)

            if start == True:
                if not fr and not fl:
                    turned_right = corner_turn(bl, br, frontr, frontl) # If it has turned right, it is initally heading north
                    if turned_right is not None:       # a turn actually happened
                        south = not turned_right           
                        start = False
                else:
                    normal_drive(frontr, frontl)

            else:
                while package_no < 2:       ### The first two packaged delivered, ends 
                    if package:
                        pole = determine_pole()
                        delivery(frontr, frontl, backl, backr, location, in_pos, pole, YN, YS)
                        in_pos = south and pole == "north" or not south and pole == "south"
                        package_no += 1
                        package = False
                    else:
                        search_for_package(frontr, frontl, backl, backr, location, in_pos)
                        package = True

                else:
                    

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


