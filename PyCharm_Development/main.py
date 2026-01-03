from asyncio import wait_for

import RPi.GPIO as GPIO
import time, math, random, queue, threading, sys, numpy as np, whisper, pyaudio, keyboard, wave, subprocess

# === GPIO Pin Definitions (BCM) ===
# Motor 1
IN1 = 23
IN2 = 24
ENA = 13  # PWM

# Motor 2
IN3 = 25
IN4 = 17
ENB = 12   # PWM

# connection to pico responsible for IR
IR_pin = 17

# connection to pico responsible for US
US_pin = 21

# === Coordinates and Orientation ===
goal = [0, 0]
my_c = [0, 0]
heading = 0   # 0=fwd, 1=right, 2=down, 3=left

# === Sensors ===
N_s = 4 #4 sensors
n = 2 #2 dimensions
#ref_s = 1 # number of reference sensor
sos = 346 #speed of sound

x_vals = [0, 3.5, -3.5, -9] # Spaltenvektoren sind Koordinaten
y_vals = [0, 4.5, 4.5, 14]
z_vals = [0, 0, 0, 0]
# 1 index is 1 cm

conversion = 3/1 #3cm per 1 step

 # === audio ===
whisper_path = "/home/liamj/whisper.cpp/build/bin/whisper-cli"
model_path = "/home/liamj/whisper.cpp/models/ggml-tiny.en.bin"

# === Orientation ===================================

fwd_stat = goal[1]
if goal[0] > 0:
    r_stat = goal[0]
    l_stat = 0
elif goal[0] < 0:
    l_stat = abs(goal[0])
    r_stat = 0
else:
    r_stat = l_stat = 0

evading = False

# === Setup command queue ==============================
cmd = queue.Queue()

# === Setup GPIO ====================================
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
duration = 2
left_gain = 0.98
right_gain = 1.00

# BCM pins for picos
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(US_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

##################Record audio################################
# === N sets of 4 datasets ===
#### audio files saved to Rbpi4:
## set1 (front right): rec11 (sensor 1), rec12 (sensor 2), rec13 (sensor 3), rec14 (sensor 4)
## set2 (front left): """"
## set3 (straight ahead): """"
## set4 (behind right): """"

#get array from audio file
FILENAME = "rec.wav"

def wav_to_array(filename):
    with wave.open(filename, 'rb') as wf:
        # Read all frames
        frames = wf.readframes(wf.getnframes())
        # Convert to numpy array
        audio_array = np.frombuffer(frames, dtype=np.int16)
    return audio_array

def get_array(set, set_nr):
    for j in range(len(set)):
        filename = f"rec{set_nr}{j+1}.wav"
        set[j] = wav_to_array(filename)
    return set

set1 = [0, 0, 0, 0]
set1 = get_array(set1, 1)

set2 = [0, 0, 0, 0]
set2 = get_array(set2, 1)

set3 = [0, 0, 0, 0]
set3 = get_array(set3, 1)

set4 = [0, 0, 0, 0]
set4 = get_array(set4, 1)

cur = set1
cur_num = 1

##############Process audio##########################################
# === Speech recognition ===
detected = False

def transcribe(filename):
    print("Transcribing...")
    result = subprocess.run(
        [whisper_path, "-m", model_path, "-f", filename, "-nt"],
        capture_output=True,
        text=True
    )
    transcription = result.stdout.strip()
    return transcription

def check_for_word(set, set_nr, word):
    is_salt = False
    for i in range(len(set)):
        filename = f"rec{set_nr}{1}.wav"
        transcript = transcribe(filename)

        if word in transcript.lower():
            is_salt = True

    if is_salt:
        return True
    else:
        return False

# === Cross correlation ===
def cc(ref_list, comp_list):

    if len(ref_list) > len(comp_list):
        for i in range(len(ref_list) - len(comp_list)):
            comp_list = np.append(comp_list, 0)
    elif len(ref_list) < len(comp_list):
        for i in range(len(comp_list) - len(ref_list)):
            ref_list = np.append(ref_list, 0)
    else:
        pass

    cc = np.correlate(ref_list, comp_list, mode='full')
    shift = np.where(cc == cc.max())[0][0] - (len(cc) // 2)
    delta_t = shift / 48000

    return delta_t

def ts(set):
    return [0, cc(set[0], set[1]), cc(set[0], set[2]), cc(set[0], set[3])]

# === Determine X_s ========= something not working

def run_X_s(t, x_vals, y_vals, z_vals):
    ref_s = 1
    #print(ref_s)

    R_iO = []
    for i in range(len(x_vals)):
        R_iO.append(math.sqrt(x_vals[i]**2+y_vals[i]**2+z_vals[i]**2))

    r_ij = np.array([((el*sos)-(t[ref_s-1]*sos)) for el in t])
    print(r_ij)


    if N_s == len(x_vals):
        print(True)
    else:
        print(False)

    S_j = np.matrix([[x_vals[el]-x_vals[ref_s-1] for el in range(len(x_vals)) if el != ref_s-1], [y_vals[el]-y_vals[ref_s-1] for el in range(len(y_vals)) if el != ref_s-1], [z_vals[el]-z_vals[ref_s-1] for el in range(len(z_vals)) if el != ref_s-1]])
    S_j = np.transpose(S_j)

    m_j = 0.5 * np.matrix([[(R_iO[el]**2) - (R_iO[ref_s-1]**2) - (r_ij[el]**2)] for el in range(N_s) if el != ref_s-1])
    print(m_j)
    print(m_j.shape)

    rho_j = np.matrix([[r_ij[el] for el in range(N_s) if el != ref_s-1]])

    D_j = np.zeros((N_s - 1, N_s - 1), float)
    for el in range(N_s):
        # print(el)
        if el != ref_s - 1:
            D_j.flat[(el - 1) * N_s] = r_ij[el]
    D_j = np.linalg.inv(D_j)

    I = np.identity(N_s-1)

    Z = np.roll(I,1, axis=1)

    M_j = (I-Z)@D_j

    X_s = np.linalg.pinv(np.transpose(S_j)@np.transpose(M_j)@M_j@S_j)@np.transpose(S_j)@np.transpose(M_j)@M_j@m_j

    return X_s[0][0].item(),X_s[1][0].item()

################# Motor + Movement ########################
# === Motor Control Functions ===
#basic logic per wheel
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

def bwd_steps(v, dur):
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

    bwd_1(v)
    bwd_2(v)

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
#movement incl. logic tracking for coordinates and direction
def step_fwd(v):
    global fwd_stat, r_stat, l_stat, heading, duration

    fwd_steps(v, duration)

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

    time.sleep(0.05)

def step_bwd(v):
    global fwd_stat, r_stat, l_stat, heading, duration

    bwd_steps(v, duration)

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

    time.sleep(0.05)

def rotate_r(v):
    global heading
    rr(v)
    time.sleep(0.05)
    heading = (heading + 1) % 4
    time.sleep(0.05)

def rotate_l(v):
    global heading
    rl(v)
    time.sleep(0.05)
    heading = (heading - 1) % 4
    time.sleep(0.05)

def oneeighty(v):
    rotate_r(v)
    rotate_r(v)
    time.sleep(0.05)

def evade_ir(v):
    global r_stat, l_stat, heading, evading

    evading = True

    step_bwd(v)
    step_bwd(v)

    if r_stat > l_stat:
        if heading == 0:
            rotate_r(v); step_fwd(v); rotate_l(v)
        elif heading == 2:
            rotate_l(v); step_fwd(v); rotate_r(v)

    elif l_stat > r_stat:
        if heading == 0:
            rotate_l(v); step_fwd(v); rotate_r(v)
        elif heading == 2:
            rotate_r(v); step_fwd(v); rotate_l(v)

    evading = False

def evade_us(v):
    global r_stat, l_stat, heading, evading

    evading = True

    oneeighty(v)
    step_fwd(v)
    oneeighty(v)

    if r_stat > l_stat and (heading == 0 or heading == 2):
        if heading == 0:
            rotate_r(v); step_fwd(v)
            rotate_l(v); step_fwd(v)
        elif heading == 2:
            rotate_l(v); step_fwd(v)
            rotate_r(v); step_fwd(v)

    elif l_stat > r_stat and (heading == 0 or heading == 2):
        if heading == 0:
            rotate_l(v); step_fwd(v)
            rotate_r(v); step_fwd(v)
        elif heading == 2:
            rotate_r(v); step_fwd(v)
            rotate_l(v); step_fwd(v)

    elif heading == 1 or heading == 3:
        rotate_l(v); step_fwd(v)
        rotate_r(v); step_fwd(v); step_fwd(v)
        rotate_r(v); step_fwd(v)
        rotate_l(v)

    evading = False


# command sequence for reaching goal, main action giver 1

def gotogoal(goal):
    global r_stat, l_stat, fwd_stat, heading, duration, evading

    if goal[1] < 0:
        cmd.put(("oneeighty", None))

    while abs(my_c[0]) < abs(goal[0]) and abs(my_c[1]) < abs(goal[1]):

        while abs(my_c[1]) < abs(goal[1]):
            if not evading:
                cmd.put(("step", speed))
                time.sleep(duration)

        if heading == 2:
            cmd.put(("oneeighty", None))

        if r_stat > 0:
            cmd.put(("rotate_r", None))
            while abs(my_c[0]) < abs(goal[0]):
                if not evading:
                    cmd.put(("step", speed))
                    time.sleep(duration)

        elif l_stat > 0:
            cmd.put(("rotate_l", None))
            while abs(my_c[0]) < abs(goal[0]):
                if not evading:
                    cmd.put(("step", speed))
                    time.sleep(duration)

# command sequence for evasion, main action giver 2 and 3

def IR_recieved(channel):
    cmd.put(("evade_ir", None))
    time.sleep(0.5)

def US_received(channel):
    cmd.put(("evade_us", None))
    time.sleep(0.5)

# recieve commands and execute

def command_loop():
        while abs(my_c[0]) < abs(goal[0]) and abs(my_c[1]) < abs(goal[1]):
            todo, val = cmd.get()

            if todo == "step":
                step_fwd(val)
            elif todo == "rotate_r":
                rotate_r(val)
            elif todo == "rotate_l":
                rotate_l(val)
            elif todo == "oneeighty":
                oneeighty(val)
            elif todo == "evade_us":
                evade_us(val)
            elif todo == "evade_ir":
                evade_ir(val)
        sys.exit()

#############################################
try:
    if check_for_word(cur, cur_num, "salt"):
        detected = True

    if detected:
        t = ts(cur)
        return1, return2 = run_X_s(t, x_vals, y_vals, z_vals)
        goal = [round(return1/conversion), round(return2/conversion)]

        GPIO.add_event_detect(IR_pin, GPIO.RISING, callback=IR_recieved, bouncetime=200)
        GPIO.add_event_detect(US_pin, GPIO.RISING, callback=US_received, bouncetime=200)
        threading.Thread(target=gotogoal, args=goal, daemon=True).start()

        command_loop()
    else:
        print("No codeword detected")

finally:
    stop_()
    GPIO.cleanup()
    print("Exiting program")