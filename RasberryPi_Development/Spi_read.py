import time
import numpy as np
import spidev as sp

bus = 0

class rbpi():
    def __init__(self, cs):
        self.device = cs
        self.spi = sp.SpiDev()
    
    def open_con(self, bus):
        self.spi.open(bus, self.device)
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0
    
    def close_con(self):
        self.spi.close()

    def reset_list(self):
        self.recorded = np.array([])

    def go(self):
        self.spi.writebytes([0x01,0x01,0x01,0x01])
    
    def stop(self):
        self.spi.writebytes([0x10,0x10,0x10,0x10])

ct = 0
pico1 = rbpi(0)
pico1.reset_list()

active_dev = pico1.device

while True:
    pico1.open_con(bus)
    #pico1.go()
    time.sleep(0.01)
    while active_dev == pico1.device and ct <= 100:
        pico1.recorded = np.append(pico1.recorded, pico1.spi.readbytes(1))
        ct += 1


    pico1.close_con()
    print(pico1.recorded)
    pico1.reset_list()
    ct = 0
    time.sleep(2)