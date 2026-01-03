import spidev
import time
import RPi.GPIO as GPIO

# CE0 -> Pico 1
spi0 = spidev.SpiDev()
spi0.open(0, 0)
spi0.max_speed_hz = 50000

spi1 = spidev.SpiDev()
spi1.open(0,0)

# CE1 -> Pico 2
DEVICE2_CS = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(DEVICE2_CS, GPIO.OUT, initial=GPIO.HIGH)

def read_pico1():
    return spi0.xfer2([1, 2, 3, 4])

def read_pico2():
    GPIO.output(DEVICE2_CS, GPIO.LOW)
    time.sleep(0.001)
    val = spi1.xfer2([1,2,3,4])
    GPIO.output(DEVICE2_CS, GPIO.HIGH)
    return val


try:
    while True:
        val0 = read_pico1()
        val1 = read_pico2()
        print(f"Device0: {val0}, Device1: {val1}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    spi0.close()
    spi1.close()
    GPIO.cleanup()
