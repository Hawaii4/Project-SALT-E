import turtle
import time
import math

# === Turtle Setup ===
t = turtle.Turtle()
t.shape("turtle")
t.color("blue")
t.speed(2)  # adjust 1–10
t.width(2)
t.left(90)

screen = turtle.Screen()
screen.title("Robot Path Simulation")
screen.setup(900, 700)

# === Initial Variables (copied exactly from your robot code) ===
goal = [30, 40]
my_c = [0, 0]
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
    l_stat = int(math.sqrt(goal[0] ** 2))
    r_stat = 0
else:
    r_stat = l_stat = 0


# === Motor Simulation (Turtle Equivalents) ===

def stop_():
    time.sleep(0.1)

def step_fwd(v):
    """Simulates one forward/backward 'motor step' visually."""
    global fwd_facing, going_back, r_facing, l_facing
    global fwd_stat, r_stat, l_stat, my_c

    # movement translation: v pixels per step
    distance = v*10

    if not going_back:
        t.forward(distance)
    else:
        t.backward(distance)

    time.sleep(0.05)

    # === coordinate logic (copied exactly) ===
    if fwd_facing and not going_back:
        my_c[1] += 1
        fwd_stat = goal[1] - my_c[1]

    elif r_facing > 0:
        my_c[0] += 1
        r_stat = goal[0] - my_c[0]

    elif l_facing > 0:
        my_c[0] -= 1
        l_stat = int(math.sqrt(goal[0] ** 2)) - int(math.sqrt(my_c[0] ** 2))

    elif not fwd_facing and going_back:
        my_c[1] -= 1
        fwd_stat = goal[1] - my_c[1]


def rotate_r(v):
    """Right rotation by 90°"""
    global r_facing, l_facing, fwd_facing, bwd_facing
    global fwd_stat, r_stat, l_stat

    t.right(90)
    time.sleep(0.05)

    r_facing += 1
    l_facing -= 1

    if (math.sqrt(l_stat ** 2) / 2) % 2 != 0 or (math.sqrt(r_stat ** 2) / 2) % 2 != 0:
        bwd_facing = True
        fwd_facing = False
    else:
        bwd_facing = False
        fwd_facing = True


def rotate_l(v):
    """Left rotation by 90°"""
    global r_facing, l_facing, fwd_facing, bwd_facing
    global fwd_stat, r_stat, l_stat

    t.left(90)
    time.sleep(0.05)

    l_facing += 1
    r_facing -= 1

    if (math.sqrt(l_stat ** 2) / 2) % 2 != 0 or (math.sqrt(r_stat ** 2) / 2) % 2 != 0:
        bwd_facing = True
        fwd_facing = False
    else:
        bwd_facing = False
        fwd_facing = True


def evade():
    """Exact same obstacle-evade logic translated to turtle movement."""
    global going_back, fwd_facing

    stop_()

    going_back = True
    fwd_facing = False
    step_fwd(1)

    going_back = False
    fwd_facing = True

    if r_stat > l_stat:          # Turn right
        rotate_r(100)
        step_fwd(1)
        rotate_l(100)

    elif r_stat < l_stat:        # Turn left
        rotate_l(100)
        step_fwd(1)
        rotate_r(100)


# === RUN EXACT SAME SEQUENCE AS THE ROBOT ===

for i in range(goal[1] - 10):
    step_fwd(1)

evade()

for i in range(10):
    step_fwd(1)

turtle.done()
