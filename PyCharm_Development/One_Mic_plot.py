import pyaudio
import wave
import keyboard
import time
import matplotlib.pyplot as plt
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
OUTPUT_FILENAME = "rec.wav"

audio = pyaudio.PyAudio()

#find out indexes of audio input devices
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=0    )

frames = []
print(" w ")
keyboard.wait("space")
print("recording")
time.sleep(0.5)

while True:
    try:
        data = stream.read(CHUNK)
        frames.append(data)
    except KeyboardInterrupt:
        break
    if keyboard.is_pressed("space"):
        print(" f   ")
        time.sleep(0.2)
        break

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(OUTPUT_FILENAME, "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

print(frames)
print(type(frames[0]))


ys = np.frombuffer(b''.join(frames), dtype=np.int16)
print(ys.tolist())
xs = np.linspace(0, len(ys)/RATE, num=len(ys))

plt.figure(figsize=(10,4))
plt.plot(xs, ys  )
plt.grid(True)
plt.show()
plt.close()