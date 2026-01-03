import spidev
import RPi.GPIO as GPIO
import time
import threading
import concurrent.futures

# Setup GPIO for manual CS
GPIO.setmode(GPIO.BCM)
DEVICE2_CS = 17
GPIO.setup(DEVICE2_CS, GPIO.OUT, initial=GPIO.HIGH)

# SPI for CE0
spi0 = spidev.SpiDev()
spi0.open(0, 0)  # Bus 0, CE0
spi0.max_speed_hz = 20000

# SPI for manual CS device (shares same bus)
spi1 = spidev.SpiDev()
spi1.open(0, 1)
spi1.max_speed_hz = 20000

def read_device_0():
    adc = spi0.xfer2([1,2,3,4])
    time.sleep(0.1)
    value = adc
    return value

def read_device_1():
    #GPIO.output(DEVICE2_CS, GPIO.LOW)  # Activate device
    adc = spi1.xfer2([1,2,3,4])
    #GPIO.output(DEVICE2_CS, GPIO.HIGH) # Deactivate device
    time.sleep(0.1)
    value = adc
    return value

try:
    while True:
        val0 = read_device_0()
        val1 = read_device_1()
        print(f"Device 0: {val0} , Device 1: {val1} ")
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    spi0.close()
    spi1.close()
    GPIO.cleanup()