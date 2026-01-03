import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
import keyboard
import time
import matplotlib.pyplot as plt
import numpy as np
import random

#Note: in this case X_s is a fixed point

speed_of_sound = 346

list1 = np.array([])
#list1 acts as reference sensor

## from one_mic_plot.py:
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

#print(frames)
#print(type(frames[0]))


ys = np.frombuffer(b''.join(frames), dtype=np.int16)
print(ys.tolist())
xs = np.linspace(0, len(ys)/RATE, num=len(ys))

plt.figure(figsize=(10,4))
plt.plot(xs, ys  )
plt.grid(True)
plt.show()
plt.close()

##

list2 = ys.tolist()
print(len(list2), "len")
for i in range(len(list2)):
    a = random.randint(-100,100)
    if (i+a) <= len(list2):
        if (i+a) >= 0:
            list1 = np.append(list1, list2[i+a] - random.randint(-300,300))
        elif (i+a) < 0:
            list1 = np.append(list1, list2[-(i+a)] - random.randint(-300, 300))
    else:
        list1 = np.append(list1, 0)

#print(list2)
print(list1, "list1")

if len(list1) > len(list2):
    for i in range(len(list1)-len(list2)):
        list2 = np.append(list2, 0)
elif len(list1) < len(list2):
    for i in range(len(list2)-len(list1)):
        list1 = np.append(list1, 0)
else:
    pass

print(list1)
print(list2)

'''
# für vergleich von binary strings folgendes verwenden
x = np.frombuffer(b'\x00\x05\x04\x03\x02\x01', dtype=np.uint8)
#dtype muss ein Vielfaches der Anzahl elemente sein in b'' (recheck, maybe other way round)
print(x)
print(np.correlate(x, list1, mode='full'))
'''

cc_12 = np.correlate(list1, list2, mode='full')
#cc_13 = np.correlate(list1, list3, mode='full')


plt.subplot(3, 1, 1)
plt.plot(list1, label='l1')
plt.plot(list2, label='l2')
#plt.plot(list3, label='l3')
plt.legend()

shift = np.where(cc_12 == cc_12.max())[0][0] - (len(cc_12)//2)
print(cc_12.max(),np.where(cc_12 == cc_12.max())[0][0])

#shift_13 = np.where(cc_13 == cc_13.max())[0][0] - (len(cc_13)//2)
#print(cc_13.max(),np.where(cc_13 == cc_13.max())[0][0])

plt.subplot(3, 1, 2)
plt.plot(list1, label='l1')
plt.plot(np.roll(list2, shift), label='l2 shifted for max correlation')
plt.legend()

'''
plt.subplot(4, 1, 3)
plt.plot(list1, label='l1')
plt.plot(np.roll(list3, shift_13), label='l3 shifted for max correlation', )
plt.legend()
'''
plt.subplot(3, 1, 3)
plt.plot(cc_12, label='cc_12')
#plt.plot(cc_13, label='cc_13')
plt.legend()

plt.plot(np.where(cc_12 == cc_12.max())[0][0], cc_12.max(), 'r+')
#plt.plot(np.where(cc_13 == cc_13.max())[0][0], cc_13.max(), 'r+')

plt.show()

print(cc_12)
#print(cc_13)
print(shift)
#print(shift_13)
print("Sampling rate: 48 kHz -> shift of {sh} indices means delay of {s} milliseconds".format(sh=shift, s=shift/48))
print("D_2 - D_1 = D_1,2 =", speed_of_sound*(shift/48000), " meters")
#print("Sampling rate: 48 kHz -> shift of {sh} indices means delay of {s} milliseconds".format(sh=shift_13, s=shift_13/48))
#print("D_3 - D_1 = D_1,3 =", speed_of_sound*(shift_13/48000), " meters")

#Test with binary strings received from One_Mic_plot.py??