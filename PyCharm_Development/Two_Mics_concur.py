import threading
import pyaudio
import wave
import keyboard
import time
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures
from datetime import datetime

ys = np.ndarray
xs = 0
ys1 = np.ndarray
xs1 = 0

class recorder:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.CHUNK = 1024
        #self.OUTPUT_FILENAME = "rec.wav"
        self.audio = pyaudio.PyAudio()
        self.t1 = datetime.now()
        self.t2 = datetime.now()

    def rec(self, name):
        print(name)
        if name == 0:
            self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK, input_device_index=0)
        elif name == 1:
            self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK, input_device_index=1)

        self.frames = []

        print("recording {name} go".format(name=name))
        self.t1 = datetime.now()
        #time.sleep(0.1) this was the problem!!!

        while not event.is_set():
            try:
                self.data = self.stream.read(self.CHUNK)
                self.frames.append(self.data)
            except KeyboardInterrupt:
                break

        time.sleep(0.1)

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.t2 = datetime.now()

        self.OUTPUT_FILENAME = "rec{name}.wav".format(name=name)

        self.waveFile = wave.open(self.OUTPUT_FILENAME, "wb")
        self.waveFile.setnchannels(self.CHANNELS)
        self.waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        self.waveFile.setframerate(self.RATE)
        self.waveFile.writeframes(b''.join(self.frames))
        self.waveFile.close()

        if name == 0:
            global ys
            ys = np.frombuffer(b''.join(self.frames), dtype=np.int16)
            global xs
            xs = np.linspace(0, len(ys) / self.RATE, num=len(ys))
        elif name == 1:
            global ys1
            ys1 = np.frombuffer(b''.join(self.frames), dtype=np.int16)
            global xs1
            xs1 = np.linspace(0, len(ys1) / self.RATE, num=len(ys1))

        print(self.t1,"time before recording//", self.t2, "time after recording //", name)

audio = pyaudio.PyAudio()
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

print("Press space to start")
keyboard.wait("space")

recs = recorder()
event = threading.Event()

with concurrent.futures.ThreadPoolExecutor() as exe:
    exe.submit(recs.rec, 0)
    exe.submit(recs.rec, 1)


    time.sleep(5)
    event_time = datetime.now()
    print(event_time, "event commencing")
    event.set()

plt.figure(figsize=(10,4))
plt.plot(xs, ys)
plt.grid(True)
plt.show()
plt.close()

plt.figure(figsize=(10,4))
plt.plot(xs1, ys1)
plt.grid(True)
plt.show()
plt.close()