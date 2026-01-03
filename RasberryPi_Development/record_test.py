import pyaudio
import wave
import time
import subprocess
import os
from pynput import keyboard
import numpy as np
import matplotlib.pyplot as plt

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000  # Recording at 16kHz directly (whisper.cpp native rate)
CHUNK = 1024
OUTPUT_FILENAME = "rec.wav"
RECORD_SECONDS = 5
WHISPER_PATH = "/home/liamj/whisper.cpp/build/bin/whisper-cli"
MODEL_PATH = "/home/liamj/whisper.cpp/models/ggml-tiny.en.bin"

print("Recording in...")
for _ in range(RECORD_SECONDS, 0, -1):
    print(_)
    time.sleep(1)
print("Recording")

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=1)

frames = []

# Record until second space press
for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording")

stream.stop_stream()
stream.close()
audio.terminate()

# Save the recording
waveFile = wave.open(OUTPUT_FILENAME, "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

ys = np.frombuffer(b''.join(frames), dtype=np.int16)
xs = np.linspace(0, len(ys)/RATE, num=len(ys))

plt.figure(figsize=(10,4))
plt.plot(xs, ys  )
plt.grid(True)
plt.show()
plt.close()