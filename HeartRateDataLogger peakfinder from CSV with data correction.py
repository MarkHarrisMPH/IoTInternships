import serial                                                   #imports the py.serial module (not a default python module)
import csv                                                      #imports csv module
import matplotlib
from scipy.signal import find_peaks                             #importing findpeaks function
matplotlib.use("TkAgg")                                         #setting backend for figure - leave this line here!
from matplotlib import pyplot as plt                            #imports polyplot module
from matplotlib.pyplot import figure                            #setting up figure
import numpy as np                                              #numpy for signal analysis

from datetime import datetime                                   #importing unixtime from os
dateTimeObj = datetime.now()                                    #getting current unixtimes
timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H-%M-%S)")      #converting unix to datetime
data = "Heartbeat "
name = data + timestampStr
filename =  "%s.csv" % name                                     #creating file with date and time


delay = 10                                                      #delay from the arduino in ms (this needs to match the arduino code!)
delay = delay/1000                                              #conversion to seconds
arduino = serial.Serial('YourCOM', 'YourBaudRate', timeout=.1)  #reads serial port (need to change for use with LoRaWAN) - change COM and baudrate accordingly

arduino.flushInput()                                            #Waits for the transmission of outgoing serial data to complete

figure(figsize =(10,5));                                        #setting dimensions of the figure


          
while True:
    try:
        ser_bytes = arduino.readline()[:-2]                     #sets data from the serial port as a variable ([:-2] is to get rid of next line character)
        
        if ser_bytes:
            ser_bytes = float(ser_bytes.decode('utf-8'))        #decodes data so that it's readable to humans
            print(ser_bytes)
            with open(filename,"a", newline ='') as f:          #creates a csv file and appends any new data to the file    
                writer = csv.writer(f,delimiter=",")            #separates data by commas
                writer.writerow([ser_bytes])                    #writes data from arduino into csv file
        

    except KeyboardInterrupt:                                   #killswitch for the script (ctrl + c)
            print("Keyboard Interrupt")                         #prints "keyboard interrupt" to python shell
            data = np.genfromtxt(filename , delimiter=",")      #finds data from csv file
            peaks, _ = find_peaks(data,height =600, prominence=20)
            plt.plot(data)
            plt.plot(peaks, data[peaks], "x")                   #plots data
            plt.xlabel("Samples per second")
            plt.ylabel("Pulse")
            distances = np.diff(peaks)                          #calculating time between peaks
            distances = distances*delay                         #accounting for milliseconds                        
            distances = 1/distances                             #calculating heartrate in hz
            
        
            bpm = (distances)*60
            #bpm calculation

            
            avgbpm = sum(bpm)//len(bpm)
            if bpm.any() > 1.2*avgbpm:                          #works out if there are any outliers
                print("Erroneous data detected")                #warning
                print(bpm)                                      #line needs to be added to remove erroneous data
                print(f'the average heart rate is {avgbpm}')
                plt.show()
                break
            else:      
                print(bpm)
                print(f'the average heart rate is {avgbpm}')
                plt.show()
                break                                           #stops the script
        
            
        
          
