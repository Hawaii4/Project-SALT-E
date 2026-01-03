from machine import Pin
import time

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
comms = Pin(5, Pin.OUT)
comms.low()

v_sound = 0.0343 #cm/us

def dist():
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        sigOff = time.ticks_us()
    while echo.value() == 1:
        sigOn = time.ticks_us()
    
    timepassed = sigOn - sigOff
    distance = timepassed * v_sound / 2
    return distance

while True:
    print("nfsdin")
    cur_dist = dist()
    if cur_dist >= 20:
        comms.high()
        time.sleep_ms(5)
        comms.low()
        print("Signal sent")
        time.sleep(4)
    time.sleep(0.05)