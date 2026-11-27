from sensor_line import main
import led

try:
    main()
finally:
    led._timer.deinit()
    led.light_turn_off(True)
