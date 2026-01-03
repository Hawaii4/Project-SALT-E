import numpy as np
import matplotlib.pyplot as plt

#Note: in this case X_s is a fixed point

speed_of_sound = 346

list1 = np.array([1,3,40,2,12,34,21,300,21,260,5])
#list1 acts as reference sensor

list2 = np.array([0,2,12,34,15,344,21,244,5])
list3 = np.array([2,20,45,9,412,50,390,20,0,0,0])

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
cc_13 = np.correlate(list1, list3, mode='full')
print(cc_12)


plt.subplot(4, 1, 1)
plt.plot(list1, label='l1')
plt.plot(list2, label='l2')
plt.plot(list3, label='l3')
plt.legend()

shift = np.where(cc_12 == cc_12.max())[0][0] - (len(cc_12)//2)
print(cc_12.max(),np.where(cc_12 == cc_12.max())[0][0])

shift_13 = np.where(cc_13 == cc_13.max())[0][0] - (len(cc_13)//2)
print(cc_13.max(),np.where(cc_13 == cc_13.max())[0][0])

plt.subplot(4, 1, 2)
plt.plot(list1, label='l1')
plt.plot(np.roll(list2, shift), label='l2 shifted for max correlation')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(list1, label='l1')
plt.plot(np.roll(list3, shift_13), label='l3 shifted for max correlation', )
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(cc_12, label='cc_12')
plt.plot(cc_13, label='cc_13')
plt.legend()

plt.plot(np.where(cc_12 == cc_12.max())[0][0], cc_12.max(), 'r+')
plt.plot(np.where(cc_13 == cc_13.max())[0][0], cc_13.max(), 'r+')

plt.show()

print(cc_12)
print(cc_13)
print(shift)
print(shift_13)
print("Sampling rate: 48 kHz -> shift of {sh} indices means delay of {s} milliseconds".format(sh=shift, s=shift/48))
print("D_2 - D_1 = D_1,2 =", speed_of_sound*(shift/48000), " meters")
print("Sampling rate: 48 kHz -> shift of {sh} indices means delay of {s} milliseconds".format(sh=shift_13, s=shift_13/48))
print("D_3 - D_1 = D_1,3 =", speed_of_sound*(shift_13/48000), " meters")

#Test with binary strings received from One_Mic_plot.py??