from machine import Pin, I2C
from VL53L0X import VL53L0X
from utime import sleep_ms

def get_distance(): #mm
    # config I2C Bus
    i2c_bus = I2C(id=0, sda=Pin(20), scl=Pin(21)) # I2C0 on GP20 & GP21
    # print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)
    
    # Setup vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)


    while True:


        # Start device
        vl53l0.start()

        # Read ten samples
        for _ in range(10):
            distance = vl53l0.read() # Check calibration!
            sleep_ms(50)

        
        # Stop device
        vl53l0.stop()

        return(distance)


while True:
    print(get_distance())
