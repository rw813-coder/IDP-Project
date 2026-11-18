class servo:

    MIN_DUTY = 1638 # 0
    MID_DUTY = 4915 # 135
    MAX_DUTY = 8192 # 270

    def __init__(self, ServoPin):
        self.servo = PWM(ServoPin)
        self.servo.freq(50)

    def set_angle(self, angle):
       # Clamp angle
       if angle < 0:
           angle = 0
       if angle > 270:
           angle = 270
 
       duty = int(servo.MIN_DUTY + (angle / 270) * (servo.MAX_DUTY - servo.MIN_DUTY))
       self.servo.duty_u16(duty)