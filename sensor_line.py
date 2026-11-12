from machine import Pin
from movements import forwards, stop, veer, normal_drive, depot_sequence, turn_90, corner_turn, yard_sequence

sens1 = 10
sens2 = 11 
sens3 = 12
sens4 = 13

frontr = Pin(sens1, Pin.IN)  ##Front right
frontl = Pin(sens2, Pin.IN)  ##Front left
backl = Pin(sens3, Pin.IN)  ##Back left
backr = Pin(sens4, Pin.IN)  ##Back right


def drive(): 

    package = False
    location = 0

    try:
        while True:
            fr = frontr.value()
            fl = frontl.value()
            bl = backl.value()
            br = backr.value()


            ### All three point states dealt with first; 
            ### Depot and yard, with events taken chronologically (for now)
            ###
            three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)

            if three_point and not package and location in (0, 1):   ###Skipping the yard initially
                location += 1
                normal_drive(fr = frontr, fl = frontl)
            
            elif three_point and not package and location == 2:   ###Entering the depot for the first time
                depot_sequence(rightturn = (br == 1), fr = frontr, fl = frontl)
                package = True

            elif three_point and package and location == 2:      ###Entering the first yard to drop off the package
                location -= 1
                yard_sequence(rightturn = (br == 1), fr = frontr, fl = frontl)
                package = False
                
            elif three_point and package and location == 1:      ###Skipping the first yard, having deposited into the second
                location -= 1
                normal_drive(fr = frontr, fl = frontl)

            ###Non-three point states
            ###

            ## Turning right/left at the corner
            elif not fr and not fl and location == 0:
                corner_turn(bl, br, frontr, frontl)
            
            ## Driving forwards normally
            elif (fr or fl) and not bl and not br:
                normal_drive(fr = frontr, fl = frontl)

            else:
                normal_drive(frontr, frontl)

    finally:
        stop()
    

if __name__ == "__main__":
    drive()
