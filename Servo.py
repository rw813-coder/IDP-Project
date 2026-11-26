from machine import Pin, PWM

class servo:

    MIN_DUTY = 1638 # 0
    MID_DUTY = 4915 # 135
    MAX_DUTY = 8192 # 270

    def __init__(self, ServoPin):
        self.servo = PWM(ServoPin)
        self.servo.freq(50)

    def set_angle(self, angle):
       # Clamp angle in degrees
       if angle < 0:
           angle = 0
       if angle > 270:
           angle = 270
 
       duty = int(servo.MIN_DUTY + (angle / 270) * (servo.MAX_DUTY - servo.MIN_DUTY))
       self.servo.duty_u16(duty)
    
    def close(self):
        self.set_angle(270)

    def open(self):
        self.set_angle(240)

    def grab(self):
        ##need grab angle from test
        self.set_angle(270)

    def high(self):
        self.set_angle(110)

    def lo(self):
        self.set_angle(185)

    def set_height(self,height):
        ##height in mm
        if height < 0:
            height = 0
        elif height > 30:
            height = 30
        duty = int(servo.MIN_DUTY + (height/ 30) * (servo.MAX_DUTY - servo.MIN_DUTY))
        self.servo.duty_u16(duty)
        return 1

g_servo_pin = 13
h_servo_pin = 15
grab_servo = servo(g_servo_pin)
height_servo = servo(h_servo_pin)