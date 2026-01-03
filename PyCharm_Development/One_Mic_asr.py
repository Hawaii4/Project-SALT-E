import pyaudio
import wave
import keyboard
import time
import whisper
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
OUTPUT_FILENAME = "rec.wav"

model = whisper.load_model("base")

audio = pyaudio.PyAudio()

'''
#find out indexes of audio input devices
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
'''

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=0)


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

data = np.frombuffer(b''.join(frames), dtype=np.uint8).astype(np.float32)

result = model.transcribe(data)
print(result["text"])

if "Salt" in result["text"]:
    print("True")

'''   
import whisper
import numpy as np

model = whisper.load_model("base")

# Example: a NumPy array of shape (n_samples,) sampled at 16000 Hz
# (You must ensure this is 16 kHz mono audio)
audio_data = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

# Then call model.transcribe() indirectly:
result = model.transcribe(audio_data)
print(result["text"])

#last changes to make program look like this from https://chatgpt.com/share/68ecf7d6-17f4-800f-b9ab-ef982afbbd40
'''