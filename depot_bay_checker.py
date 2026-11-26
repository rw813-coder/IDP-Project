def new_depot_sequence(rightturn, fr, fl, bl, br, entry = False, upper = False):
    'Turns into depot, picks up package, and exits depot'
    if entry:
        turn_90(rightturn, fr, fl)  #Turn into depot
        rotate_time(rightturn, True, 90)
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
        turn_90(rightturn, frontr, frontl)           #Turn the opposite way as in entry to the depot
    else:                                                                                                                                    
        depot_drive(fr, fl, bl, br, reversing = True)    #Reverse until the three-point junction 
        turn_90(not rightturn, frontr, frontl)      #Turn the same way as in entry to the depot     
    return package_found    

def depot_bay_checker():
    'Checks all the bays in the depot until package is found'
    bay_no = 0
    while True:
        found = new_depot_sequence(rightturn, frontr, frontl, backl, backr, entry = bay_no == 1)
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
