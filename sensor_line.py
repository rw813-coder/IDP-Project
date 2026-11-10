from machine import Pin
sens1 = ##
sens2 = ## 
sens3 = ##
sens4 = ##
line_sensor1 = Pin(sens1, Pin.IN)
line_sensor2 = Pin(sens2, Pin.IN)
line_sensor3 = Pin(sens3, Pin.IN)
line_sensor4 = Pin(sens4, Pin.IN)
forward_state = line_sensor1.value() and \
line_sensor2.value() ==1 and line_sensor3.value() \
and line_sensor4.value() == 0
while forward_state == True:
    print("Moving Forward")
    forward_state = 