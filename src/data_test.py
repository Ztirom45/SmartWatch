from random import randint
from SaveData3 import readFromDisk
from zlm import *

a = list(map(lambda i: abs(i[0]), filter(lambda i: i!= [], readFromDisk("f"))))
#a = list(map(lambda a:math.sin(a/5)+randint(-5,5)/10,range(100)))

#get peaks
peak_filter = lambda position: is_peak(a,position)
peaks_pos = list(map(lambda i:i,filter(peak_filter,range(len(a)))))
peaks_val = list(map(lambda i:a[i],peaks_pos))

steps = 0
for i in range(0,len(peaks_pos)-2,2):#later in a main loop
            #get freq and amp of first step
            step_freq = (max((a[peaks_pos[i]],a[peaks_pos[i+1]]))-
                        min((a[peaks_pos[i]],a[peaks_pos[i+1]])))
            step_amp = max(peaks_pos[i:i+2])-min(peaks_pos[i:i+2])
            if step_freq > 0.3:
                        print(step_freq,step_amp)
                        steps += 1
print(steps)

import matplotlib.pyplot as plt
    

plt.plot(a)
plt.plot(peaks_pos,peaks_val)
plt.show()
