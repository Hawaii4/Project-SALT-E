#combine Motors_evade_sim & Motors_gotogoal_sim.py
import turtle, time, math, random, queue

# === Setup Turtle Environment ===
t = turtle.Turtle()
t.shape("turtle")
t.color("blue")
t.speed(8)  # Adjust for realism (1 = slowest, 10 = fast)
t.left(90)

# Optional: Draw coordinate grid
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Robot Path Simulation")

# === Initial Conditions ===
goal = [50, 50]
my_c = [0, 0]
'''
r_facing = 0
l_facing = 0
fwd_facing = True
bwd_facing = False
if fwd_stat < 0:
    going_back = True
else:
    going_back = False
    
-> replace with 1 variable
'''
heading = 0 # fwd = 0, 1 = right, 2 = down, 3 = left

goal_marker = turtle.Turtle()
goal_marker.penup()
goal_marker.goto(goal[0]*1, goal[1]*1)
goal_marker.dot(10, "red")

# Translate coordinates like in your code
fwd_stat = goal[1]
if goal[0] > 0:
    r_stat = goal[0]
    l_stat = 0
elif goal[0] < 0:
    l_stat =  abs(goal[0])
    r_stat = 0
else:
    r_stat = l_stat = 0

print(fwd_stat, r_stat, l_stat)

# setup command queue
cmd = queue.Queue()

# === Movement Simulation Functions ===
def stop_():
    """Simulate stop (do nothing)"""
    time.sleep(0.2)


def step_fwd(v):
    """Simulate one forward step"""
    global fwd_stat, r_stat, l_stat, heading

    t.forward(v)

    if heading == 0:
        #t.forward(v)
        # fwd_stat -= 1
        my_c[1] += 1
        fwd_stat = goal[1] - my_c[1]
    elif heading == 1:
        #t.forward(v)
        # r_stat -= 1
        my_c[0] += 1
        r_stat = goal[0] - my_c[0]
    elif heading == 3:
        #t.forward(v)
        # l_stat -= 1
        my_c[0] -= 1
        l_stat =  abs(goal[0]) -  abs(my_c[0])
    elif heading == 2:
        #t.forward(v)
        # fwd_stat += 1
        my_c[1] -= 1
        fwd_stat = goal[1] - my_c[1]
    print(my_c)



def rotate_r():
    """Rotate right by 90 degrees"""
    global heading, fwd_stat, r_stat, l_stat
    t.right(90)
    time.sleep(0.2)

    heading = (heading + 1) % 4


def rotate_l():
    """Rotate left by 90 degrees"""
    global heading, fwd_stat, r_stat, l_stat
    t.left(90)
    time.sleep(0.2)

    heading = (heading - 1) % 4

def oneeighty():
    for i in range(2):
        rotate_r()

def gotogoal(v):
    global r_stat, l_stat, fwd_stat, heading
    """Simulate robot going to target coordinates"""
    if goal[1] < 0:
        oneeighty()

    while my_c[0] < abs(goal[0]) and my_c[1] < abs(goal[1]):
        while abs(my_c[1]) < abs(goal[1]):
            step_fwd(v)
            time.sleep(0.05)
        else:
            pass

        if heading == 2:
            oneeighty()

        if r_stat > 0:
            rotate_r()
            while abs(my_c[0]) < abs(goal[0]):
                step_fwd(v)
                time.sleep(0.05)
            else:
                pass
        elif l_stat > 0:
            rotate_l()
            while abs(my_c[0]) <  abs(goal[0]):
                step_fwd(v)
                time.sleep(0.05)
            else:
                pass



def evade():
    global   fwd_stat, r_stat, l_stat


    stop_()
    oneeighty()
    step_fwd(1)
    oneeighty()

    if r_stat > l_stat:          # Turn right
        print(r_stat, l_stat)
        if heading == 0:
            rotate_r()
            step_fwd(1)
            rotate_l()
            step_fwd(1)
        elif heading == 2:
            rotate_l()
            step_fwd(1)
            rotate_r()
            step_fwd(1)
        print("done")

    elif r_stat < l_stat:        # Turn left
        print(r_stat, l_stat)
        if heading == 0:
            rotate_l()
            step_fwd(1)
            rotate_r()
            step_fwd(1)
        elif heading == 2:
            rotate_r()
            step_fwd(1)
            rotate_l()
            step_fwd(1)
        print("done")
    else:
        print("error")

    #change stats

def evade_sim():
    if (random.randint(0,100) %2) == 0:
        evade()
    time.sleep(0.1)
# === Run Simulation ===
gotogoal(1)


print(my_c)

# Keep window open
turtle.done()

#chatgpt generated from Motors_gotogoal https://chatgpt.com/share/6911ba0b-f468-800f-926a-5d33983fd70b