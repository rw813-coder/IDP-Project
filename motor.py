from machine import Pin, PWM

  
class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
            
    def off(self):
        self.pwm.duty_u16(0)
            
    def normal_speed(self, speed=60):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def veer_speed(self, speed = 40):
        self.mDir.value(0)                     # slower speed in the direction of the veer
        self.pwm.duty_u16(int(65535 * speed / 100))  

    def turn_speed(self, speed=30):            # slower turn speed, will change this value later
        self.mDir.value(0)
        self.pwm.duty_u16(int(65535 * speed / 100))

    def reverse(self, speed=30):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))


left_motor = Motor(dirPin=7, PWMPin=6)  # left motor
right_motor = Motor(dirPin=4, PWMPin=5)  # right motor
