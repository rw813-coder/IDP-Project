def delivery(frontr, frontl, backl, backr, location, in_pos, pole, YN, YS):
    'Delivers the first and second packages, requires package = True and package_no to be 0 or 1'
    correct_side = in_pos
    fr, fl, bl, br = frontr.value(), frontl.value(), backl.value(), backr.value()
    three_point = three_point = (fr and fl and bl and not br) or (fr and fl and br and not bl)
    if correct_side:
        target = YN + 1 if pole == "north" else YS + 1
        if three_point and location == target:
            yard_sequence(br == 1, fr, fl, bl, br)
            break
            #Package no += 1, package = False, and redefines in_pos after exiting
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
            junction_function()
            correct_side = True
        else:
            if three_point:
                skip_three_point()
                location -= 1
            elif not fr and not fl:
                corner_turn(bl, br, frontr, frontl)
            else:
                normal_drive(frontr, frontl)


def search_for_package(fr, fl, bl, br, location, in_pos):
    'Searches for the first and second packages, requires package = False and package_no to be 0 or 1 to run'
    correct_side = in_pos
    three_point = three_point = (fr.value() and fl.value() and bl.value() and not br.value()) \
    or (fr.value() and fl.value() and br.value() and not bl.value())
    if correct_side:
        if three_point and location == 3:
            new_depot_sequence()
            break
            #package = True after exiting
        else:
            normal_drive()
            if three_point:
                skip_three_point()
                location += 1
    else:
        if three_point and location == 0:
            junction_function(fr, fl, bl, br)
            correct_side = True
        else:
            normal_drive()
            if three_point:
                skip_three_point()
                location -= 1








