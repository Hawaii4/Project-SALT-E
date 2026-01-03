import pyaudio
import wave
import time
import subprocess
import os
from pynput import keyboard
import numpy as np

FILENAME = "rec.wav"

def wav_to_array(filename):
    with wave.open(filename, 'rb') as wf:
        # Read all frames
        frames = wf.readframes(wf.getnframes())
        # Convert to numpy array
        audio_array = np.frombuffer(frames, dtype=np.int16)
    return audio_array

print(wav_to_array("rec.wav"))