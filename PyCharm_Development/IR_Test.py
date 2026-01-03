import RPi.GPIO as GPIO
import time

IR_pin = 27
ct = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def go():
    global ct
    print("Detected")
    ct += 1

GPIO.add_event_detect(IR_pin, GPIO.RISING, callback=go, bouncetime=200)

try:
    while ct <= 10:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
