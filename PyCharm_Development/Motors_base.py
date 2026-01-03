import RPi.GPIO as GPIO
import time

# === GPIO Pin Definitions (BCM) ===
# Motor 1
IN1 = 12
IN2 = 11
ENA = 13  # PWM

# Motor 2
IN3 = 7
IN4 = 6
ENB = 8   # PWM

# === Setup GPIO ===
GPIO.setmode(GPIO.BCM)

# Direction pins
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# PWM pins
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Create PWM objects at 1 kHz
pwm_a = GPIO.PWM(ENA, 1000)
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0)
pwm_b.start(0)

# === Helper to convert MicroPython duty_u16 (0-65535) to 0-100% ===
def scale_speed(speed_u16):
    return max(0, min(100, (speed_u16 / 65535) * 100))

# === Motor Control Functions ===
def fwd_1(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(scale_speed(speed))

def bwd_1(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(scale_speed(speed))

def fwd_2(speed):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_b.ChangeDutyCycle(scale_speed(speed))

def bwd_2(speed):
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_b.ChangeDutyCycle(scale_speed(speed))

def stop_():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

# === Main Loop ===
try:
    while True:
        print("down (rechts)")
        bwd_1(15000)
        fwd_2(15000)
        time.sleep(1)

        print("up (links)")
        bwd_2(15000)
        fwd_1(15000)
        time.sleep(1)

        print("left (vorwärts)")
        bwd_1(30000)
        bwd_2(30000)
        time.sleep(1)

        print("right (rückwärts)")
        fwd_1(30000)
        fwd_2(30000)
        time.sleep(1)

        stop_()
        time.sleep(0.5)

except KeyboardInterrupt:
    stop_()
    GPIO.cleanup()
    print("Exiting program")


#base code converted from micropython with chatgpt https://chatgpt.com/share/6910c48f-7618-800f-9cec-27338091de34
