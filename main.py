import RPi.GPIO as GPIO
from datetime import datetime
import time

# Pump pumps 2.4 L per minute
pump = 11
lamp = 13

# water_voltage = 12
water_low = 18
water_high = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(lamp, GPIO.OUT)
GPIO.setup(water_low, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(water_high, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(pump, True)

timeout = 0

try:
    while True:

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if now.hour < 8 or now.hour > 18:
            mode = "night"
        else:
            mode = "day"

        if mode == "day":
            GPIO.output(lamp, False)
        else:
            GPIO.output(lamp, True)
# Water amount in mL
        water_amount = 250
        water_time = water_amount / (2400 / 60)
# Potential to implement Fluid level checking and Fluid level adjustments
        while mode == "day":
            # False means switch closed
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if GPIO.input(water_low) == False:
                timeout = time.time() + water_time
                #GPIO.output(pump, False)
                print("water low")
            if GPIO.input(water_high) == False or time.time() > timeout:
                #GPIO.output(pump, True)
                print("water high")

            if now.hour < 8 or now.hour >= 18:
                mode = "night"
            else:
                mode = "day"
            # Check every second as not to hog CPU
            time.sleep(1)
finally:
    GPIO.cleanup()

