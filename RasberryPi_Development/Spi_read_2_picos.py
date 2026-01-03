import time
import numpy as np
import spidev as sp
import threading
import concurrent.futures

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
    
    def read(self, bus):
        while not event.is_set():
            try:
                self.open_con(bus)
                self.recorded = np.append(self.recorded, self.spi.readbytes(10))
                self.close_con()
            except KeyboardInterrupt:
                break

pico1 = rbpi(0)
pico1.reset_list()

pico2 = rbpi(1)
pico2.reset_list()


event = threading.Event()
'''
with concurrent.futures.ThreadPoolExecutor() as exe:
    exe.submit(pico1.read, bus)
    exe.submit(pico2.read, bus)

    print("go")

    time.sleep(10)
    event.set()
'''

print(pico1.recorded)
print(pico2.recorded)