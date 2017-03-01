#!/usr/bin/python

import MPU6050
import math
import time
import numpy

#TargetSampleNumber= 1024
#TargetRate =  33    # frequency =  8000 / ( integr value + 1)  minimum frequency=32,25

InputSampleRate = 33#raw_input("Sample Rate(32.25 ... 2000) ?")
InputSampleNumber = 1024 #raw_input("Number of sample to take ?")    

TargetSampleNumber= int(InputSampleNumber)
TargetRate= float(InputSampleRate)



mpu6050 = MPU6050.MPU6050()

mpu6050.setup()
mpu6050.setGResolution(2)
mpu6050.setSampleRate(TargetRate)
mpu6050.enableFifo(False)
time.sleep(0.01)

print "Capturing {0} samples at {1} samples/sec".format(TargetSampleNumber, mpu6050.SampleRate)

raw_input("Press enter to start")

mpu6050.resetFifo()
mpu6050.enableFifo(True)
time.sleep(0.01)

Values = []
Total = 0

while True:


 if mpu6050.fifoCount == 0:
     Status= mpu6050.readStatus()

     # print "Status",Status
     if (Status & 0x10) == 0x10 :
        print "Overrun Error! Quitting.\n"
        quit()

     if (Status & 0x01) == 0x01:
        Values.extend(mpu6050.readDataFromFifo())
 
 else:
        Values.extend(mpu6050.readDataFromFifo())

 #read Total number of data taken
 Total = len(Values)/14
 # print Total
 if Total >= TargetSampleNumber :
   break;
print Values
 