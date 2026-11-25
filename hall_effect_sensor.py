import machine
import time
from initialization import wait_ms

adc = machine.ADC(machine.Pin(28)) # initialising ADC reading

def read_adc_voltage():
    'Reads the voltage from the hall effect sensor'

    raw = adc.read_u16() # reads the analog to digital output as a 16 bit integer

    voltage = (raw/65535)*3.3 # converts 16 bit integer to voltage (reference is 3.3V)

    return voltage

def determine_pole():
    'reads the pole of a magnet near the sensor. returns "north", "south", or "neither"'
    north_threshold = 2.2 # lower bound for a magnetic north pole

    south_threshold = 1.9 # upper bound for a magnetic south pole

    voltage = read_adc_voltage() # reads voltage from the hall effect sensor

    #checks what the voltage corresponds to
    
    if voltage >= north_threshold:
        return "north"
    elif voltage <= south_threshold:
        return "south"
    else:
        return "neither"

def package_present(samples=5, delay_ms=40):
    'Sample the hall sensor over 200 ms, to check for magnetic field at a depot'
    for _ in range(samples):
        if determine_pole() != "neither":
            return True
        wait_ms(delay_ms)
    return False

# while True:
#     x = determine_pole()
#     print(x)
#     time.sleep_ms(75)