from machine import Pin, ADC
import time, sys

aOut = ADC(Pin(27))
comms = Pin(5, Pin.OUT)
comms.low()

while True:
    print(aOut.read_u16())
    if aOut.read_u16() >= 30000:
        comms.high()
        time.sleep_ms(5)
        comms.low()
        print("Signal sent")
        time.sleep(4)
    time.sleep_ms(50)
