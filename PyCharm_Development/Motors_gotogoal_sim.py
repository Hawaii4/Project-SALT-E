import turtle
import time
import math

# === Setup Turtle Environment ===
t = turtle.Turtle()
t.shape("turtle")
t.color("blue")
t.speed(5)  # Adjust for realism (1 = slowest, 10 = fast)
t.left(90)

# Optional: Draw coordinate grid
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Robot Path Simulation")

# === Initial Conditions ===
goal = [50, 50]
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

goal_marker = turtle.Turtle()
goal_marker.penup()
goal_marker.goto(goal[0]*1, goal[1]*1)
goal_marker.dot(10, "red")

# Translate coordinates like in your code
if goal[0] > 0:
    r_stat = goal[0]
    l_stat = 0
elif goal[0] < 0:
    l_stat = int(math.sqrt(goal[0]**2))
    r_stat = 0
else:
    r_stat = l_stat = 0

print(fwd_stat, l_stat, r_stat)


# === Movement Simulation Functions ===
def stop_():
    """Simulate stop (do nothing)"""
    time.sleep(0.2)


def step_fwd(v):
    """Simulate one forward step"""
    global fwd_facing, going_back, r_facing, l_facing, fwd_stat, r_stat, l_stat

    if not going_back:
        t.forward(v) # Move turtle forward
    elif going_back:
        t.backward(v)

    if fwd_facing and not going_back:
        # fwd_stat -= 1
        my_c[1] += 1
        fwd_stat = goal[1] - my_c[1]
    elif r_facing > 0:
        # r_stat -= 1
        my_c[0] += 1
        r_stat = goal[0] - my_c[0]
    elif l_facing > 0:
        # l_stat -= 1
        my_c[0] -= 1
        l_stat = int(math.sqrt(goal[0] ** 2)) - int(math.sqrt(my_c[0] ** 2))
    elif not fwd_facing and going_back:
        # fwd_stat += 1
        my_c[1] -= 1
        fwd_stat = goal[1] - my_c[1]


def rotate_r(v):
    """Rotate right by 90 degrees"""
    global r_facing, l_facing, fwd_facing, bwd_facing, fwd_stat, r_stat, l_stat
    t.right(90)
    time.sleep(0.2)

    r_facing += 1
    l_facing -= 1

    if (math.sqrt(l_stat**2) / 2) % 2 != 0 or (math.sqrt(r_stat**2) / 2) % 2 != 0:
        bwd_facing = True
        fwd_facing = False
    elif (math.sqrt(l_stat**2) / 2) % 2 == 0 or (math.sqrt(r_stat**2) / 2) % 2 == 0:
        bwd_facing = False
        fwd_facing = True
    else:
        bwd_facing = False
        fwd_facing = False


def rotate_l(v):
    """Rotate left by 90 degrees"""
    global r_facing, l_facing, fwd_facing, bwd_facing, fwd_stat, r_stat, l_stat
    t.left(90)
    time.sleep(0.2)

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
    """Simulate robot going to target coordinates"""
    for i in range(int(math.sqrt(fwd_stat**2))):
        step_fwd(v)
        time.sleep(0.05)
    going_back = False
    if r_stat > 0:
        rotate_r(v)
        print(r_facing)
        for j in range(r_stat):
            step_fwd(v)
            print(r_facing)
            time.sleep(0.05)
    elif l_stat > 0:
        rotate_l(v)
        for j in range(l_stat):
            step_fwd(v)
            time.sleep(0.05)

# === Run Simulation ===
gotogoal(1)
print(my_c)
print(fwd_stat, r_facing, r_stat)


# Keep window open
turtle.done()

#chatgpt generated from Motors_gotogoal https://chatgpt.com/share/6911ba0b-f468-800f-926a-5d33983fd70b
