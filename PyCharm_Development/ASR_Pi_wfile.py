import pyaudio
import wave
import subprocess
import time
from pathlib import Path
import numpy as np
from pynput import keyboard

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
OUTPUT_FILENAME = "rec.wav"

Whisper_bin = "./whisper.cpp/main"
Whisper_model = "./whisper.cpp/models/ggml-tiny.en.bin"

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=0)


frames = []
recording = False

def on_press(key):
    global recording
    if key == keyboard.Key.space:
        recording = not recording
        if recording:
            print("Recording...")
        else:
            print("Stopped")

listener = keyboard.Listener(on_press=on_press)
listener.start()

# Wait for recording to start
while not recording:
    time.sleep(0.1)

while recording:
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)

listener.stop()

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(OUTPUT_FILENAME, "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

cmd = [Whisper_bin,
    "-m", Whisper_model,
    "-f", OUTPUT_FILENAME,
    "--output-txt",
    "--language", "en"]

subprocess.run(cmd, check=True)

txt_file = Path(OUTPUT_FILENAME).with_suffix(".txt")
text = txt_file.read_text().strip()

print("Transcript:", text)

if "Salt" in text:
    print("True")


# keyboard input doesn't work on RbPi -> see code on RbPi for 5 second recording window