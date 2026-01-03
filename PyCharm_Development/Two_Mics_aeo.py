import pyaudio
import wave
import keyboard
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
OUTPUT_FILENAME = "rec.wav"
OUTPUT_FILENAME_2 = "rec2.wav"

audio = pyaudio.PyAudio()

#find out indexes of audio input devices
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=1)

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

audio2 = pyaudio.PyAudio()
stream2 = audio2.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=0)

frames = []
print(" w ")
keyboard.wait("space")
print("recording")
time.sleep(0.5)

while True:
    try:
        data = stream2.read(CHUNK)
        frames.append(data)
    except KeyboardInterrupt:
        break
    if keyboard.is_pressed("space"):
        print(" f   ")
        time.sleep(0.2)
        break

stream2.stop_stream()
stream2.close()
audio2.terminate()

waveFile2 = wave.open(OUTPUT_FILENAME_2, "wb")
waveFile2.setnchannels(CHANNELS)
waveFile2.setsampwidth(audio.get_sample_size(FORMAT))
waveFile2.setframerate(RATE)
waveFile2.writeframes(b''.join(frames))
waveFile2.close()
