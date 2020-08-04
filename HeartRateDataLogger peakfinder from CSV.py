import os                                                       #user input
import serial                                                   #imports the py.serial module (not a default python module)
import csv                                                      #imports csv module
import time                                                     #time stamp in unix time from computer (may or may not need to use it)
import matplotlib
from scipy.signal import find_peaks                             #importing findpeaks function
matplotlib.use("TkAgg")                                         #setting backend - leave this line here!
from matplotlib import pyplot as plt                            #imports polyplot module
from matplotlib.pyplot import figure                            #setting up figure
import numpy as np                                              #numpy for signal analysis

delay = float(input("Please enter delay from arduino\n"))       #user input for delay from arduino (may need hard coding later)
print(f'You have entered {delay}')
delay = delay/1000
arduino = serial.Serial('COM5', 9600, timeout=.1)               #reads serial port (need to change for LoRaWAN)

arduino.flushInput()                                            #Waits for the transmission of outgoing serial data to complete
os.remove("Heartbeat.csv")                                      #deletes file before rewriting new data
figure(figsize =(10,5));


          
while True:
    try:
        ser_bytes = arduino.readline()[:-2]                     #sets data from the serial port as a variable ([:-2] is to get rid of next line character)
        
        if ser_bytes:
            ser_bytes = float(ser_bytes.decode('utf-8'))        #decodes data so that it's readable to humans
            print(ser_bytes)
            with open("Heartbeat.csv","a", newline ='') as f:   #creates a csv file and appends any new data to the file    
                writer = csv.writer(f,delimiter=",")            #separates data by commas
                writer.writerow([ser_bytes])                    #writes data from arduino into csv file
        

    except KeyboardInterrupt:                                   #killswitch for the script (ctrl + c)
            print("Keyboard Interrupt")                         #prints "keyboard interrupt" to python shell
            data = np.genfromtxt("Heartbeat.csv", delimiter=",")#finds data from csv file
            peaks, _ = find_peaks(data)
            plt.plot(data)
            plt.plot(peaks, data[peaks], "x")                   #plots data            
            distances = np.diff(peaks)                          #calculating time between peaks
            distances = distances*delay                         #accounting for milliseconds                        
            distances = 1/distances                             #calculating heartrate in hz
    
        #if:distance(n-1)=/=distance(n)*0.9                    #detecting atrial fibrilation, may need some correctional factor for adjustment
            #print("AF Detected!")                             #i.e if the distance before isn't within some %age of the next one then it's AF
            
        #or:distance(n-1)=/= distance(n)*1.1
            #print("AF Detected!")

            bpm = (distances)*60                                #bpm calculation
            avgbpm = sum(bpm)/len(bpm)
            print(f'the average heart rate is {avgbpm}')
            plt.show()
            break                                               #stops the script
        
            
        
          
