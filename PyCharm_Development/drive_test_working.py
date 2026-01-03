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
ENB = 12  # PWM

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

speed = 46
left_gain = 0.98
right_gain = 1.00


# === Motor Control Functions ===
# basic logic per wheel
def fwd_1(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)


def bwd_1(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)


def fwd_2(speed):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)


def bwd_2(speed):
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)


def stop_():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    time.sleep(2)


# basic logic coordinated two wheels
def fwd(v):
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    # effective distance moved forward =!= conversion
    fwd_1(v)
    fwd_2(v)

    pwm_a.ChangeDutyCycle(v * left_gain)
    pwm_b.ChangeDutyCycle(v * right_gain)

    time.sleep(0.5)
    stop_()


def fwd_steps(v, dur):
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

    fwd_1(v)
    fwd_2(v)

    ramp_steps = 8
    for i in range(5, ramp_steps + 1):
        duty = v * i / ramp_steps
        pwm_a.ChangeDutyCycle(duty * left_gain)
        pwm_b.ChangeDutyCycle(duty * right_gain)
        time.sleep(dur / ramp_steps)

    stop_()
    time.sleep(0.5)


def rr(v):
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

    fwd_1(v)
    bwd_2(v)

    pwm_a.ChangeDutyCycle(v * left_gain / 4)
    pwm_b.ChangeDutyCycle(v * right_gain / 4)

    time.sleep(0.5)
    stop_()


def rl(v):
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

    bwd_1(v)
    fwd_2(v)

    pwm_a.ChangeDutyCycle(v * left_gain / 4)
    pwm_b.ChangeDutyCycle(v * right_gain / 4)

    time.sleep(0.5)
    stop_()


def main():
    fwd_steps(speed, 1)


# distance for 1 fwd_steps() is roughly 3-3.5 cm


main()

# changes from test2: pwm ramping up -> better / more controllable for lower speeds
# https://chatgpt.com/share/693ee1d2-bee8-800f-8876-1ab159cd28f7