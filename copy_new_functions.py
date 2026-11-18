def junction_function(fr, fl, br, bl, upwards = False):
    flag = 0
    while True:
        if upwards:
            rv, lv, brv, blv = fr.value(), fl.value(), br.value(), bl.value()
            correction(rv, lv)
            if not brv and not blv:
                flag += 1
            elif flag == 1 and (brv or blv):
                turn_90(rightturn = (brv == 1), fr, fl)            
        else:
            rv, lv, brv, blv = fr.value(), fl.value(), br.value(), bl.value()
            correction(rv, lv)
            if not brv and not blv and flag == 0:
                flag += 1
            elif flag == 1 and brv and blv:
                flag += 1
            elif flag == 2 and not brv and not blv:
                break
            else:
                continue

    stop()

def upwards_entry(fr, fl, br, bl, target, rightdirection = True):
    position = 0
    rv, lv, brv, blv = fr.value(), fl.value(), br.value(), bl.value()
    while True:
        normal_drive(fr, fl)
        if brv and blv and position < 0:
            position += 1
            continue
        elif position == target:           ###has reached the target depot, now needs to execute depot sequence and go back to jnc
            depot_sequence(rightdirection, fr, fl, br, bl)
            normal_drive(fr, fl)           ###the start of the return
            if brv and blv and position > 0:
                position -= 1
                continue
            elif position == 0 and brv and blv: ###reaches junction
                break
            else:
                continue
        else:
            continue

def depot_sequence(rightturn, fr, fl, bl, br, depot):
    'Turns into depot, picks up package, and exits depot'
    turn_90(rightturn, fr, fl)  #Turn into depot
    depot_drive(fr, fl, bl, br)         #Drive until line ends
    if determine_pole() == 'neither':
        stop()
        depot_drive(fr, fl, bl, br, reversing = True)          #Reverse until the three-point junction
        turn_90(not rightturn, fr, fl)               #Turn the opposite way as in entry to the depot
            depot[0] += 1                                         #continue and increment depot state
    else:
        stop()                              #Stop to pick up package
        time.sleep_ms(3000)                                   
        depot_drive(fr, fl, bl, br, reversing = True)          #Reverse until the three-point junction
        turn_90(rightturn, fr, fl)               #Turn the same way as in entry to the depot
            depot[1] = True                                     #Make sure to set depot state to True

DGR, DGL, DUR, DUL = [0, False], [0, False], [0, False], [0, False] 
## Initial depot stattes, loop will continue for an individual depot until [6, -] or [-, True]