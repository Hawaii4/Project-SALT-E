import RPi.GPIO as GPIO
import time, math

#note: fwd/bwd functions -> one pin high other low -> does this mean only one wheel spins at a time?

goal = [30,40]
my_c = [0,0]
r_facing = 0
l_facing = 0
fwd_stat = goal[1]
fwd_facing = True
bwd_facing = False
if fwd_stat < 0:
    going_back = True
else:
    going_back = False

if goal[0] > 0:
    r_stat = goal[0]
    l_stat = 0
elif goal[0] < 0:
    l_stat = int(math.sqrt(goal[0]**2))
    r_stat = 0
else:
    r_stat = l_stat = 0

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

def step_fwd(v):
    global fwd_facing, going_back, r_facing, l_facing, fwd_stat, r_stat, l_stat

    if not going_back:
        fwd_1(v)
        fwd_2(v)
        time.sleep(1)
        stop_()
    elif going_back:
        bwd_1(v)
        bwd_2(v)
        time.sleep(1)
        stop_()

    if fwd_facing and not going_back:
        #fwd_stat -= 1
        my_c[1] += 1
        fwd_stat = goal[1] - my_c[1]
    elif r_facing > 0:
        #r_stat -= 1
        my_c[0] += 1
        r_stat = goal[0] - my_c[0]
    elif l_facing > 0:
        #l_stat -= 1
        my_c[0] -= 1
        l_stat = int(math.sqrt(goal[0]**2)) - int(math.sqrt(my_c[0]**2))
    elif not fwd_facing and going_back:
        #fwd_stat += 1
        my_c[1] -= 1
        fwd_stat = goal[1] - my_c[1]

def rotate_r(v):
    global r_facing, l_facing, fwd_facing, bwd_facing, fwd_stat, r_stat, l_stat

    fwd_1(v)
    bwd_2(v)
    time.sleep(0.5)
    stop_()

    r_facing += 1
    l_facing -= 1

    if (math.sqrt(l_stat ** 2) / 2) % 2 != 0 or (math.sqrt(r_stat ** 2) / 2) % 2 != 0:
        bwd_facing = True
        fwd_facing = False
    elif (math.sqrt(l_stat ** 2) / 2) % 2 == 0 or (math.sqrt(r_stat ** 2) / 2) % 2 == 0:
        bwd_facing = False
        fwd_facing = True
    else:
        bwd_facing = False
        fwd_facing = False

def rotate_l(v):
    global r_facing, l_facing, fwd_facing, bwd_facing, fwd_stat, r_stat, l_stat

    fwd_2(v)
    bwd_1(v)
    time.sleep(0.5)
    stop_()

    l_facing += 1
    r_facing -= 1

    if (math.sqrt(l_stat ** 2) / 2) % 2 != 0 or (math.sqrt(r_stat ** 2) / 2) % 2 != 0:
        bwd_facing = True
        fwd_facing = False
    elif (math.sqrt(l_stat ** 2) / 2) % 2 == 0 or (math.sqrt(r_stat ** 2) / 2) % 2 == 0:
        bwd_facing = False
        fwd_facing = True
    else:
        bwd_facing = False
        fwd_facing = False

def gotogoal(v):
    global r_stat, l_stat, fwd_stat, going_back

    for i in range(int(math.sqrt(fwd_stat ** 2))):
        step_fwd(v)
        time.sleep(0.05)
    going_back = False
    if r_stat > 0:
        rotate_r(v//2)
        print(r_facing)
        for j in range(r_stat):
            step_fwd(v)
            print(r_facing)
            time.sleep(0.05)
    elif l_stat > 0:
        rotate_l(v//2)
        for j in range(l_stat):
            step_fwd(v)
            time.sleep(0.05)

gotogoal(100)