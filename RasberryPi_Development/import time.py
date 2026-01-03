import time
import spidev as sp

bus = 0

class rbpi():
    def __init__(self, cs):
        self.devie = cs
        self.recorded = []
        self.spi = sp.SpiDev()
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0
    
    def open_con(self, bus):
        self.spi.open(bus, self.device)
    
    def close_con(self):
        self.spi.close()

ct = 0
pico1 = rbpi(0)

active_dev = pico1.device

pico1.open_con(bus)
while active_dev == pico1.device and ct <= 100:
    pico1.recorded.append(pico1.spi.read(1))
    ct += 1