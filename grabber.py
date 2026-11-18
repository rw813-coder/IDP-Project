from machine import Pin, PWM

class servo:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)
        self.pwm = PWM(Pin(PWMPin))
        self.pwm.freq(1000)  
        self.pwm.duty_u16(0)  
        self.speed = 0