# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 19:00:20 2016

@author: sarve
"""

import wave
import sys
import random
import math
 
audio_file = wave.open(sys.argv[1], 'r')
file_key = int(sys.argv[2])
 
#random.seed(int(private_key))
 
recovery_factor = audio_file.getnframes() // (file_key)
spread = math.floor(recovery_factor / 2)
n = 0
buf = bytearray(audio_file.readframes(recovery_factor))
while len(buf) > 0:
    d = 0
    for i in range(8):
        f_byte = int(i * spread)# + random.randint(0, spread - 1))
        if f_byte % 2 == 1:
            f_byte -= 1
        if(len(buf)<=f_byte):
            f_byte=int(f_byte/len(buf))
        d += (buf[f_byte] % 2) << i
        #print(d)
    
    print("decoded: ", d)
    n += 1
    if n >= file_key:
        break
    buf = bytearray(audio_file.readframes(recovery_factor))
