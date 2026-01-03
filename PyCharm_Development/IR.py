import RPi.GPIO as GPIO
import time

SIGNAL_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def signal_detected(channel):
    print("IR Signal received")  # This will print every time the pin goes HIGH

# Rising edge detection
GPIO.add_event_detect(SIGNAL_PIN, GPIO.RISING, callback=signal_detected, bouncetime=200)

print("Waiting for signal from Pico...")

try:
    while True:
        # Keep program running so the callback can trigger
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
