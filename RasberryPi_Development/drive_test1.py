import RPi.GPIO as GPIO
import time, math, random, queue, threading, sys, numpy as np

# === GPIO Pin Definitions (BCM) ===
# Motor 1
IN1 = 23
IN2 = 24
ENA = 13  # PWM

# Motor 2
IN3 = 25
IN4 = 17
ENB = 12   # PWM

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

speed = 40

# === Motor Control Functions ===
#basic logic per wheel
def fwd_1(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)

def bwd_1(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)

def fwd_2(speed):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_b.ChangeDutyCycle(speed)

def bwd_2(speed):
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_b.ChangeDutyCycle(speed)

def stop_():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

#basic logic coordinated two wheels
def fwd(v):
    # effective distance moved forward =!= conversion
    fwd_1(v); fwd_2(v); time.sleep(0.5)
    stop_()

def rr():
    fwd_1(speed); bwd_2(speed); time.sleep(0.5)
    stop_()

def rl():
    bwd_1(speed); fwd_2(speed); time.sleep(0.5)
    stop_()



def main():
    for i in range(5):
        fwd(speed)


main()