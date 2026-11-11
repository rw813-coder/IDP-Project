from machine import Pin
from movements import forwards, turn_90, veer, depot_sequence, corner_turn


def run(): 
    package = False
    location = 0 ### 0 is between the junction and the deposit, 1 is in between the two deposits,
    #### 2 is between the deposit and the depot - i.e. entering, in, and exiting the depot

    loading_area_approaching = True
    junction = True
    #### Depot_state = 0

    sens1 = ##
    sens2 = ## 
    sens3 = ##
    sens4 = ##

    line_sensor1 = Pin(sens1, Pin.IN)  ##Front right
    line_sensor2 = Pin(sens2, Pin.IN)  ##Front left
    line_sensor3 = Pin(sens3, Pin.IN)  ##Back left
    line_sensor4 = Pin(sens4, Pin.IN)  ##Back right

    ### Move forwards
    forward_state = line_sensor1.value() and \
    line_sensor2.value() and line_sensor3.value() == 0\
    and line_sensor4.value() == 0
    while forward_state == True:
        print("Moving Forward")
        forwards()

    ## Veering left; FR has gone to zero
    veer_left_state = line_sensor1.value() == 0 and \
    line_sensor2.value() == 1 and line_sensor3.value() == 0\
    and line_sensor4.value() == 0
    while veer_left_state == True:
        print("Veering left")
        veer(veerright = False)


    ## Veering right; FL has gone to zero
    veer_right_state = line_sensor1.value() and \
    line_sensor2.value() == 0 and line_sensor3.value() == 0\
    and line_sensor4.value() == 0
    while veer_right_state == True:
        print("Veering right")
        veer()


    ## 90 degree turns at corners
    corner_state = line_sensor1.value() == 0 and \
    line_sensor2.value() == 0 and location == 0

    if corner_state == 1:
        corner_turn(bl = line_sensor3.value(), br = line_sensor4.value(), \
        fr = line_sensor1.value(), fl = line_sensor2.value())
        forwards()

####################################################################################
##Turning at tri_points, this is defined by whether
##we are entering the depot or deposit, and whether
##there is a package or not
##
## three_point state with BL = 1
three_point_left_state = line_sensor1.value() and \
line_sensor2.value() and line_sensor3.value()\
and line_sensor4.value() == 0

## three_point state with BR = 1
three_point_right_state = line_sensor1.value() and \
line_sensor2.value() and line_sensor3.value() == 0\
and line_sensor4.value()

##Turning into depot sequence, LEFT turns
if three_point_left_state == True and package == False and \
location == 2:
    depot_sequence(rightturn = False)

##Turning into depot sequence, RIGHT turns
if three_point_right_state == True and package == False and \
location == 2:
    depot_sequence()

##Turning into deposit sequence, LEFT turns
if three_point_left_state == True and package == True and \
location == 2:
    deposit_sequence(rightturn = False)

    
