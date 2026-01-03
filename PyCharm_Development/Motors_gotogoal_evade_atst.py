import RPi.GPIO as GPIO
import time, math, random, queue, threading, sys

# === GPIO Pin Definitions (BCM) ===
# Motor 1
IN1 = 12
IN2 = 11
ENA = 13  # PWM

# Motor 2
IN3 = 7
IN4 = 6
ENB = 8   # PWM

# connection to pico responsible for IR
IR_pin = 17

# connection to pico responsible for US
US_pin = 21

# === Coordinates and Orientation ===
goal = [-50, 50]
my_c = [0, 0]
heading = 0   # 0=fwd, 1=right, 2=down, 3=left

fwd_stat = goal[1]
if goal[0] > 0:
    r_stat = goal[0]
    l_stat = 0
elif goal[0] < 0:
    l_stat = abs(goal[0])
    r_stat = 0
else:
    r_stat = l_stat = 0

# === Setup command queue ===
cmd = queue.Queue()

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

# BCM pins for picos
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(US_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# === Helper to convert MicroPython duty_u16 (0-65535) to 0-100% ===
def scale_speed(speed_u16):
    return max(0, min(100, (speed_u16 / 65535) * 100))

# === Motor Control Functions ===
#basic logic per wheel
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

#basic logic coordinated two wheels
def fwd(v):
    fwd_1(v); fwd_2(v); time.sleep(0.5)
    stop_()

def rr():
    fwd_1(100); bwd_2(100); time.sleep(0.5)
    stop_()

def rl():
    bwd_1(100); fwd_2(100); time.sleep(0.5)
    stop_()

#movement incl. logic tracking for coordinates and direction
def step_fwd(v):
    global fwd_stat, r_stat, l_stat, heading

    fwd(v)

    if heading == 0:
        my_c[1] += 1
        fwd_stat = goal[1] - my_c[1]
    elif heading == 1:
        my_c[0] += 1
        r_stat = goal[0] - my_c[0]
    elif heading == 3:
        my_c[0] -= 1
        l_stat = abs(goal[0]) - abs(my_c[0])
    elif heading == 2:
        my_c[1] -= 1
        fwd_stat = goal[1] - my_c[1]

def rotate_r():
    global heading
    rr()
    time.sleep(0.05)
    heading = (heading + 1) % 4

def rotate_l():
    global heading
    rl()
    time.sleep(0.05)
    heading = (heading - 1) % 4

def oneeighty():
    rotate_r()
    rotate_r()

def evade():
    global r_stat, l_stat, heading

    oneeighty()
    step_fwd(100)
    oneeighty()

    if r_stat > l_stat and (heading == 0 or heading == 2):
        if heading == 0:
            rotate_r(); step_fwd(100)
            rotate_l(); step_fwd(100)
        elif heading == 2:
            rotate_l(); step_fwd(100)
            rotate_r(); step_fwd(100)

    elif l_stat > r_stat and (heading == 0 or heading == 2):
        if heading == 0:
            rotate_l(); step_fwd(100)
            rotate_r(); step_fwd(100)
        elif heading == 2:
            rotate_r(); step_fwd(100)
            rotate_l(); step_fwd(100)

    elif heading == 1 or heading == 3:
        rotate_l(); step_fwd(100)
        rotate_r(); step_fwd(100); step_fwd(100)
        rotate_r(); step_fwd(100)
        rotate_l()


# command sequence for reaching goal, main action giver 1

def gotogoal():
    global r_stat, l_stat, fwd_stat, heading

    if goal[1] < 0:
        cmd.put(("oneeighty", None))

    while abs(my_c[0]) < abs(goal[0]) and abs(my_c[1]) < abs(goal[1]):

        while abs(my_c[1]) < abs(goal[1]):
            cmd.put(("step", 100))
            time.sleep(0.5)

        if heading == 2:
            cmd.put(("oneeighty", None))

        if r_stat > 0:
            cmd.put(("rotate_r", None))
            while abs(my_c[0]) < abs(goal[0]):
                cmd.put(("step", 100))
                time.sleep(0.5)

        elif l_stat > 0:
            cmd.put(("rotate_l", None))
            while abs(my_c[0]) < abs(goal[0]):
                cmd.put(("step", 100))
                time.sleep(0.5)

# command sequence for evasion, main action giver 2 and 3

def IR_recieved(channel):
    cmd.put(("evade", None))

def US_received(channel):
    cmd.put(("evade", None))

# recieve commands and execute

def command_loop():
        while my_c != goal:
            todo, val = cmd.get()

            if todo == "step":
                step_fwd(val)
            elif todo == "rotate_r":
                rotate_r()
            elif todo == "rotate_l":
                rotate_l()
            elif todo == "oneeighty":
                oneeighty()
            elif todo == "evade":
                evade()
        sys.exit()

#############################################
try:
    GPIO.add_event_detect(IR_pin, GPIO.RISING, callback=IR_recieved, bouncetime=200)
    GPIO.add_event_detect(US_pin, GPIO.RISING, callback=US_received, bouncetime=200)
    threading.Thread(target=gotogoal, daemon=True).start()

    command_loop()

except KeyboardInterrupt or sys.exit():
    stop_()
    GPIO.cleanup()
    print("Exiting program")