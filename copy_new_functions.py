def delivery(fr, fl, bl, br, location, in_pos, pole, YN, YS):
    'Delivers the first and second packages, requires package = True and package_no to be 0 or 1'
    correct_side = in_pos
    if correct_side:
        target = YN + 1 if pole == "north" else YS + 1
        if location == target:
            yard_sequence()
            break
            #Package no += 1, package = False, and redefines in_pos after exiting
        else:
            normal_drive()
            if three_point:
                skip_three_point()
                location += 1
    else:
        if location == 0:
            junction_function()
            correct_side = True
        else:
            normal_drive()
            if three_point:
                skip_three_point()
                location -= 1


def search_for_package(fr, fl, bl, br, location, in_pos):
    'Searches for the first and second packages, requires package = False and package_no to be 0 or 1 to run'
    correct_side = in_pos
    if correct_side:
        if location == 3:
            depot_sequence()
            break
            #package = True after exiting
        else:
            normal_drive()
            if three_point:
                skip_three_point()
                location += 1
    else:
        if location == 0:
            junction_function()
            correct_side = True
        else:
            normal_drive()
            if three_point:
                skip_three_point()
                location -= 1








