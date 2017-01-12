# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 19:00:20 2016

@author: sarve
"""

import wave
import sys
import random
import os
import math
import numpy as np
import matplotlib.pyplot as plt
 
def PSNR(original, modified):
    #print(len(original), len(modified))
    maximum = 255
    size = len(original)
    MSE = np.sum(pow(original[i] - modified[i], 2) for i in range(size))/size
    PSNR = 10*np.log10(maximum*maximum/MSE)
    return PSNR

 
 
def plotit(x,y, fig, xlabel, ylabel, title):
    #For plotting the error graphs 
    plt.figure(1)           #figure number
    plt.plot(x, y)          #pass the X and Y values to be plotted
    plt.xlabel(xlabel)      #Label for X axis
    plt.ylabel(ylabel)      #Label for Y axis
    plt.title(title)        #Give the Plot a title
    #plt.show()              #Display the graph


# Input Format "python program.py audio_file hidden_file dest_file"     
audio_file = wave.open(sys.argv[1], 'r')
hidden_file = open(sys.argv[2], 'r')

file_size = os.path.getsize(sys.argv[2])
spreading_factor = audio_file.getnframes()  // (file_size)

# Print the size of encoded file followed by no of frames
print ("Encoding File Size: " + str(file_size))
print ("No of Frames in Audio Input: " + str(audio_file.getnframes()))

init_buff = []

# Minimum no of frames of audio signal is 60 to be able to encode a message
if spreading_factor >= 60:
    spread = math.floor(spreading_factor / 2)
    #print ("Spreading Factor: ",spreading_factor)
      
    init_buff = audio_file.readframes(-1)
    init_buff = [item+0 for item in init_buff]
    audio_file.setpos(0)
    mod_buff = []

    while True: 
            dest_file = wave.open(sys.argv[3], 'w')
 
            # Set details of Output file to that of Input file
            dest_file.setnchannels(audio_file.getnchannels())
            dest_file.setsampwidth(audio_file.getsampwidth())
            dest_file.setframerate(audio_file.getframerate())
            dest_file.setnframes(audio_file.getnframes())

            user_choice = "y"
            if(user_choice.lower() == "yes" or user_choice.lower() == "y"):
                  # Read n frames from the audio signal
                  buf = bytearray(audio_file.readframes(spreading_factor))
                  buflen = len(buf)
                  #print(buflen)
                  while(len(buf) > 0):
                        data = hidden_file.read(1)
                        
                        if data:
                              data = ord(data)
                              #print(data)
                              for i in range(8):
                                    #print(str(data) + "::" + str(i))
                                    bit = data >> i
                                    #print (bit)
                                    f_byte = int(i * spread)# + random.randint(0,spread - 1))
                                    #print("F_BYTE: " + str(f_byte))
	
                                    if f_byte % 2 == 1:
                                          f_byte -=1

                                    if(f_byte >= buflen):
                                          f_byte=int(f_byte/buflen)

                                    if buf[f_byte] % 2 == 0 and bit % 2 == 1:
                                          buf[f_byte] += 1
                                    elif buf[f_byte] % 2 == 1 and bit % 2 == 0:
                                          buf[f_byte] -= 1
                        try:
                              mod_buff.extend(buf)
                              
                              dest_file.writeframes(buf)
                              buf = bytearray(audio_file.readframes(spreading_factor))
                        except wave.Error as e:
                              print(str(e))

                  print ("The Spreading Factor is ", spreading_factor * 4)
                  dest_file.close()
                  break
            elif user_choice.lower() == "no" or user_choice.lower() == "n":
                  print ("Proceed to exit")
                  break
            else:
                  print ("Please enter yes or no")            
    

    print("PSNR: ", PSNR(init_buff, mod_buff))
    plotit(list(range(5000)), init_buff[:5000], 1, 'time', 'amplitude', 'Original')
    plotit(list(range(5000)), mod_buff[:5000], 1, 'time', 'amplitude', 'Steg')  
    plt.show()
    print("DONE")

else:
    print ("Is NOT enough to continue, you need a bigger wav file")
 
hidden_file.close()
audio_file.close()
