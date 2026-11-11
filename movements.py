from global_data import wheelbase, wheeltrack
from motor import left_motor, right_motor

def movementsrun():

    def forwards():
        left_motor.normal_speed()
        right_motor.normal_speed()

    def turn_90(rightturn, fr, fl):
        if rightturn == True:
            while fl == False:
                left_motor.turn_speed()
                right_motor.reverse()
            else:
                return
        else:
            while fr == False:
                left_motor.reverse()
                right_motor.turn_speed()
            else:
                return
    
    def corner_turn(bl, br, fr, fl):
        while bl == False and br == False:
            forwards()
        else:
            turn_90(rightturn = br, fr = fr, fl = fl)

    def veer(veerright = True):
        if veerright:
            left_motor.normal_speed()
            right_motor.veer_speed()
        else:
            left_motor.veer_speed()
            right_motor.normal_speed()

if __name__ == "__main__":
    movementsrun()



####################
def depot_sequence(rightturn, fr, fl): 
    turn_90(rightturn = rightturn)
    while fr = True and fl = True:
        forwards()
    else:
        package = 1
    ###reverse
    turn_90(rightturn = not rightturn) 
    ###drive forwards
    return 1

def deposit_sequence(rightturn = True):
    return 1