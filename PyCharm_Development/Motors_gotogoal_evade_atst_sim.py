# === Combined Motors_evade_sim & Motors_gotogoal_sim (thread-safe) ===
import turtle, time, math, random, queue, threading, sys

# === Turtle setup ===
t = turtle.Turtle()
t.shape("turtle")
t.color("blue")
t.speed(0)             # fastest drawing
t.left(90)

screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Robot Path Simulation")

# === Initial State ===
goal = [random.randint(-100,100), random.randint(-100,100)]
my_c = [0, 0]
heading = 0   # 0=fwd, 1=right, 2=down, 3=left

goal_marker = turtle.Turtle()
goal_marker.penup()
goal_marker.goto(goal[0], goal[1])
goal_marker.dot(10, "red")

# translated coordinates like your program
fwd_stat = goal[1]
if goal[0] > 0:
    r_stat = goal[0]
    l_stat = 0
elif goal[0] < 0:
    l_stat = abs(goal[0])
    r_stat = 0
else:
    r_stat = l_stat = 0

print(fwd_stat, r_stat, l_stat)

# === COMMAND QUEUE ===
cmd = queue.Queue()


# ============================================================
#   MOVEMENT + ROTATION (executed ONLY in main thread)
# ============================================================

def step_fwd(v):
    global fwd_stat, r_stat, l_stat, heading

    t.forward(v)

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

    print(my_c)


def rotate_r():
    global heading
    t.right(90)
    time.sleep(0.05)
    heading = (heading + 1) % 4


def rotate_l():
    global heading
    t.left(90)
    time.sleep(0.05)
    heading = (heading - 1) % 4


def oneeighty():
    rotate_r()
    rotate_r()


# ============================================================
#   PARALLEL THREAD: gotogoal() — produces commands
# ============================================================

def gotogoal_thread():
    global r_stat, l_stat, fwd_stat, heading

    if goal[1] < 0:
        cmd.put(("oneeighty", None))

    while abs(my_c[0]) < abs(goal[0]) and abs(my_c[1]) < abs(goal[1]):

        while abs(my_c[1]) < abs(goal[1]):
            cmd.put(("step", 1))
            time.sleep(0.5)

        if heading == 2:
            cmd.put(("oneeighty", None))

        if r_stat > 0:
            cmd.put(("rotate_r", None))
            while abs(my_c[0]) < abs(goal[0]):
                cmd.put(("step", 1))
                time.sleep(0.5)

        elif l_stat > 0:
            cmd.put(("rotate_l", None))
            while abs(my_c[0]) < abs(goal[0]):
                cmd.put(("step", 1))
                time.sleep(0.5)

# ============================================================
#   PARALLEL THREAD: evade_sim() — randomly triggers evade()
# ============================================================

def evade_sim_thread():
    while True:
        if (random.randint(0, 100) % 2) == 0:
            cmd.put(("evade", None))
        time.sleep(0.5)


def evade():
    global r_stat, l_stat

    oneeighty()
    step_fwd(1)
    oneeighty()

    if r_stat > l_stat and (heading == 0 or heading == 2):
        if heading == 0:
            rotate_r(); step_fwd(1)
            rotate_l(); step_fwd(1)
        elif heading == 2:
            rotate_l(); step_fwd(1)
            rotate_r(); step_fwd(1)

    elif l_stat > r_stat and (heading == 0 or heading == 2):
        if heading == 0:
            rotate_l(); step_fwd(1)
            rotate_r(); step_fwd(1)
        elif heading == 2:
            rotate_r(); step_fwd(1)
            rotate_l(); step_fwd(1)

    elif heading == 1 or heading == 3:
        rotate_l(); step_fwd(1)
        rotate_r(); step_fwd(1); step_fwd(1)
        rotate_r(); step_fwd(1)
        rotate_l()


# ============================================================
#   MAIN THREAD COMMAND LOOP — executes turtle actions
# ============================================================

def command_loop():
    try:
        while my_c != goal:
            todo, val = cmd.get_nowait()

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

    except queue.Empty:
        pass

    screen.ontimer(command_loop, 1)  # FAST execution


# ============================================================
#   START THREADS + BEGIN COMMAND LOOP
# ============================================================

threading.Thread(target=gotogoal_thread, daemon=True).start()
threading.Thread(target=evade_sim_thread, daemon=True).start()

command_loop()       # start command processor
turtle.done()
