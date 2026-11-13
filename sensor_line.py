from machine import Pin
from movements import stop, normal_drive, corner_turn, depot_sequence, yard_sequence
import time
from led import light_flash

sens1 = 8
sens2 = 9 
sens3 = 10
sens4 = 11

frontr = Pin(sens1, Pin.IN)  ##Front right
frontl = Pin(sens2, Pin.IN)  ##Front left
backl = Pin(sens3, Pin.IN)  ##Back left
backr = Pin(sens4, Pin.IN)  ##Back right

def skip_three_point():
    while backl.value() or backr.value():
        normal_drive(frontr, frontl)
        light_flash()

def drive(): 

    package = False
    location = 0
    last_location = 0

    try:
        while True:

            light_flash()

            if location != last_location:
                print("location: ", location)
                last_location = location
                            
            fr = frontr.value()
            fl = frontl.value()
            bl = backl.value()
            br = backr.value()


            ### All three point states dealt with first; 
            ### Depot and yard, with events taken chronologically (for now)
            ###
            three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)

            if three_point and not package and location == 0:   ###Skipping the yard initially
                skip_three_point()
                location += 1

            elif three_point and not package and location == 1:   ###Skipping the yard initially
                skip_three_point()
                location += 1

            elif three_point and not package and location == 2:   ###Skipping the yard initially
                skip_three_point()
                location += 1
            
            elif three_point and not package and location == 3:   ###Entering the depot for the first time
                depot_sequence(rightturn = (br == 1), fr = frontr, fl = frontl, bl = backl, br = backr)
                package = True

            elif three_point and package and location == 3:      ###Entering the first yard to drop off the package
                location -= 1
                yard_sequence(rightturn = (br == 1), fr = frontr, fl = frontl, bl = backl, br = backr)
                package = False

            elif three_point and not package and location == 2:   ###Skipping the yard initially
                skip_three_point()
                location -= 1

            elif three_point and not package and location == 1:   ###Skipping the yard initially
                skip_three_point()
                location -= 1
    
            elif three_point and package and location == 1:      ###Not used, package should become false
                skip_three_point()
                location -= 1

            ###Non-three point states
            ###

            ## Turning right/left at the corner
            elif not fr and not fl:
                corner_turn(bl, br, frontr, frontl)
            
            ## Driving forwards normally
            else:
                normal_drive(frontr, frontl)

    finally:
        stop()
    
# def readings():
#         while True:
#             print(frontr.value(), frontl.value(), backl.value(), backr.value())
#             time.sleep(0.2)

if __name__ == "__main__":
    drive()
