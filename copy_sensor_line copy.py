from machine import Pin
from movements import stop, normal_drive, corner_turn, depot_sequence, yard_sequence, new_depot_sequence
import time
from initialization import button_pressed

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
right = True
package_no = 0
location = 1
increment = False
DGS, DGN, DUS, DUN = True, True, True, True
## Represents the bay number visited, and whether or not the package has been collected
## Bay numbers go from 0 to 5. These correspond to locations 3 to 8.

def skip_three_point():
    while backl.value() or backr.value():
        normal_drive(frontr, frontl)

def drive(): 
    global package, location, increment, DGR, DGL, DUR, DUL
 
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

            ### All three point states dealt with first; 
            ### Depot and yard, with events taken chronologically (for now)
            ###
            three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)

            if three_point and not package and location == 0:
                if increment:
                    stop()
                    break  #Junction mode would go here, and, because package = false, would skip the three points at locations 1 and 2
                else:
                    skip_three_point()
                    location += 1

            elif three_point and not package and location in range(1, 3):   ###Skipping the yard initially
                skip_three_point()
                if increment:
                    location -= 1
                else:
                    location += 1
            
            elif three_point and not package and location in range(3, 9):   ###Entering the depot for the first time
                package_found = new_depot_sequence(rightturn = (br == 1), fr = frontr, fl = frontl, bl = backl, br = backr)
                skip_three_point()
                if package_found:
                    package = True
                    location -= 1
                else:
                    location += 1

            elif three_point and package and location in range(3, 9):
                skip_three_point()
                location -= 1

            elif three_point and package and location == 2:      ###Entering the first yard to drop off the package
                package = False
                location -= 1
                increment = True
                yard_sequence(rightturn = (br == 1), fr = frontr, fl = frontl, bl = backl, br = backr)

            ##Non-three point states
            ## Turning right/left at the corner
            elif not fr and not fl:
                corner_turn(bl, br, frontr, frontl)
            
            ## Driving forwards normally
            else:
                normal_drive(frontr, frontl)

    finally:
        stop()
    
def reset_state():
    global location, package
    package = False
    location = 0
    for d in (DGS, DGN, DUS, DUN):
        d = False

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


