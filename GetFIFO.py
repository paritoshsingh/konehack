#!/usr/bin/python
import MySQLdb
import MPU6050
import math
import time
import numpy
import paho.mqtt.client as mqtt
import json
import uuid
import smbus
from datetime import datetime

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


#TargetSampleNumber= 1024
#TargetRate =  33    # frequency =  8000 / ( integr value + 1)  minimum frequency=32,25

InputSampleRate = 128#raw_input("Sample Rate(32.25 ... 2000) ?")
InputSampleNumber = 512 #raw_input("Number of sample to take ?")    

TargetSampleNumber= int(InputSampleNumber)
TargetRate= float(InputSampleRate)



mpu6050 = MPU6050.MPU6050()

mpu6050.setup()
mpu6050.setGResolution(2)
mpu6050.setSampleRate(TargetRate)
mpu6050.enableFifo(False)
time.sleep(0.01)

print "Capturing {0} samples at {1} samples/sec".format(TargetSampleNumber, mpu6050.SampleRate)

mpu6050.resetFifo()
mpu6050.enableFifo(True)
time.sleep(0.01)

Values = []
Total = 0
#Set the variables for connecting to the iot service
broker = ""
deviceId="gyro-pi1" #you can give the    address as default also
topic = "iot-2/evt/status/fmt/json"
username = "use-token-auth"
password = "gyropiauth" #auth-token
organization = "lscroe" #org_id
deviceType = "accel"

topic = "iot-2/evt/status/fmt/json"

#Creating the client connection
#Set clientID and broker
clientID = "d:" + organization + ":" + deviceType + ":" + deviceId
broker = organization + ".messaging.internetofthings.ibmcloud.com"
mqttc = mqtt.Client(clientID)

#Set authentication values, if connecting to registered service
if username is not "":
  mqttc.username_pw_set(username, password=password)

mqttc.connect(host=broker, port=1883, keepalive=60)
#Publishing to IBM Internet of Things Foundation
mqttc.loop_start()


while True:
 if mpu6050.fifoCount == 0:
     Status= mpu6050.readStatus()

     # print "Status",Status
     if (Status & 0x10) == 0x10 :
        print "Overrun Error! Quitting.\n"
        quit()

     if (Status & 0x01) == 0x01:
        start_time=time.time()
        Values.extend(mpu6050.readDataFromFifo())
 
 else:
        start_time=time.time()
        Values.extend(mpu6050.readDataFromFifo())

 #read Total number of data taken
 Total = len(Values)/14
 # print Total
 if Total >= TargetSampleNumber :
   break;
 
 db = MySQLdb.connect("localhost", "root", "funk", "pidata")
 curs=db.cursor()
 print mpu6050.convertData(Values)


for loop in range (TargetSampleNumber):
    SimpleSample = Values[loop*14 : loop*14+14]
    I = mpu6050.convertData(SimpleSample)
    
    gyro_xout_scaled =(I.Gyrox)
    gyro_yout_scaled =(I.Gyroy)
    gyro_zout_scaled =(I.Gyroz)

    accel_xout = I.Gx
    accel_yout = I.Gy
    accel_zout = I.Gz
    accel_xout_scaled = accel_xout
    accel_yout_scaled = accel_yout
    accel_zout_scaled = accel_zout
    x_rotation=get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    y_rotation=get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    time_stamp=start_time + float(loop*((time.time()-start_time)/TargetSampleNumber))

    msg = json.JSONEncoder().encode({"d":{"measured_timestamp":time_stamp, "accel_xout_scaled":accel_xout_scaled, "accel_yout_scaled":accel_yout_scaled, "accel_zout_scaled":accel_zout_scaled}})
    mqttc.publish(topic, payload=msg, qos=1, retain=False)
      

 


 
