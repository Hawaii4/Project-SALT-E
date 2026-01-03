import numpy as np
import matplotlib.pyplot as plt

list1 = np.array([0,1,1,3,3,4,4,5,5,7,7])

list2 = np.array([0,0,0,0,0,1,1,2,2,4,4,6,6,8,8])

cc_12 = np.correlate(list1, list2, mode='full')

print(list1)
print(list2)
print(cc_12)

speed_of_sound = 346

plt.subplot(3, 1, 1)
plt.plot(list1, label='l1')
plt.plot(list2, label='l2')
plt.legend()

shift = np.where(cc_12 == cc_12.max())[0][0] - (len(cc_12)//2)
print(cc_12.max(),np.where(cc_12 == cc_12.max())[0][0])

plt.subplot(3, 1, 2)
plt.plot(list1, label='l1')
plt.plot(np.roll(list2, shift), label='l2 für R_xy maximal')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(cc_12, label='cc_12')
plt.legend()

plt.plot(np.where(cc_12 == cc_12.max())[0][0], cc_12.max(), 'r+')

plt.show()

print(cc_12)
print(shift)
print("Sampling rate: 48 kHz -> shift of {sh} indices means delay of {s} milliseconds".format(sh=shift, s=shift/48))
print("D_2 - D_1 = D_1,2 =", speed_of_sound*(shift/48000), " meters")
#Test with binary strings received from One_Mic_plot.py??