from sensor_line import main
import led

try:
    main()
finally:
    led._timer.deinit()
    led.light_turn_off(True)

# from machine import Pin
# from utime import sleep

# #Set the LED pin and configuration
# led_pin = 18
# led = Pin(led_pin, Pin.OUT)

# #Set the button pin
# button_pin = 22
# button = Pin(button_pin, Pin.IN)

# #Continiously update the LED value and print said value
# while True:
#   led.value(button.value())
#   sleep(0.1)
#   print(button.value())


