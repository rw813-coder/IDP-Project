def junction_function(fr, fl, bl, br, upwards = False):
    flag = 0
    while True:
        rv, lv, blv, brv = fr.value(), fl.value(), bl.value(), br.value()
        correction(rv, lv)                               #Using correction as it takes .value() created within the function
                                                         #Could use normal_drive with the fr, fl, bl, br inputs instead
        if upwards:
            if flag == 0 and not brv and not blv:
                flag = 1
            elif flag == 1 and (brv or blv):
                time.sleep_ms(50)
                blv, brv = bl.value(), br.value()   #Re-read sensors after the sleep
                if blv and brv:
                    turn_90(determine_pole() == "north", fr, fl)
                    break
                else:
                    turn_90(brv == 1, fr, fl)
                    break            
        else:
            if not brv and not blv and flag == 0:
                flag += 1
            elif flag == 1 and brv and blv:
                flag += 1
            elif flag == 2 and not brv and not blv:
                break
    stop()

def upper_depots(fr, fl, bl, br, rightdirection = True):
    pos = 0
    package = False
    on_four_point = False            # True while still sitting on a four point already counted

    while True:
        blv, brv = bl.value(), br.value()
        new_four_point = bool(blv and brv)  #Triggers every time both of the rear sensors are 1

        if not new_four_point:
            on_four_point = False    # left the junction, so the next one counts as new

        if new_four_point and not on_four_point:
            on_four_point = True     # latch: handle each junction once

            if not package:
                if pos < 6:
                    package = new_depot_sequence(rightdirection, fr, fl, bl, br)
                    if not package:
                        pos += 1

            else:
                pos -= 1           
                if pos <= 0:      #junction has been reached
                    break

        normal_drive(fr, fl)       # reads the front sensors itself
                                   # Using normal_drive as it takes the pin objects (frontr etc) directly

    stop()
    return pos


def new_depot_sequence(rightturn, fr, fl, bl, br):
    'Turns into depot, picks up package, and exits depot'
    turn_90(rightturn, fr, fl)  #Turn into depot
    depot_drive(fr, fl, bl, br)         #Drive until line ends
    package_found = not (determine_pole() == 'neither')
    if package_found:
        stop()
        time.sleep_ms(3000)                                #Pick up the package
        depot_drive(fr, fl, bl, br, reversing = True)          #Reverse until the three-point junction
        turn_90(not rightturn, fr, fl)               #Turn the opposite way as in entry to the depot
                                      # Go deliver the package
    else:
        stop()                                                        
        depot_drive(fr, fl, bl, br, reversing = True)          #Reverse until the three-point junction
        turn_90(rightturn, fr, fl)               #Turn the same way as in entry to the depot 
    return package_found