import machine
import time

def read_adc_voltage(pin = 28):
    'Reads the voltage from the hall effect sensor'
    adc = machine.ADC(machine.Pin(pin)) # initialising ADC reading

    raw = adc.read_u16() # reads the analog to digital output as a 16 bit integer

    voltage = (raw/65535)*3.3 # converts 16 bit integer to voltage (reference is 3.3V)

    return voltage

def determine_pole(pin = 28):
    'reads the pole of a magnet near the sensor. returns "north", "south", or "neither"'
    north_threshold = 2.2 # lower bound for a magnetic north pole

    south_threshold = 1.9 # upper bound for a magnetic south pole

    voltage = read_adc_voltage(pin) # reads voltage from the hall effect sensor

    #checks what the voltage corresponds to
    
    if voltage >= north_threshold:
        return "north"
    elif voltage <= south_threshold:
        return "south"
    else:
        return "neither"