import pyserial
import time
import paho.mqtt.client as mqtt
import json
import uuid
import smbus
import math
from datetime import datetime

#opening serial port
ser=serial.Serial('/dev/ttyACM0')
#Set the variables for connecting to the iot service
broker = ""
deviceId="gyro-pi1" #you can give the 	 address as default also
topic = "iot-2/evt/arduino/fmt/json"
username = "use-token-auth"
password = "gyropiauth" #auth-token
organization = "blve66" #org_id
deviceType = "gyro-pi"

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

while mqttc.loop() == 0:
	analog_in = ser.readline().split()

	accel_xout = int(analog_in[0])
	accel_yout = int(analog_in[1])
	accel_zout = int(analog_in[2])
	accel_xout_scaled = 9.8*(accel_xout-350 / 350)
	accel_yout_scaled = 9.8*(accel_yout-350 / 350)
	accel_zout_scaled = 9.8*(accel_zout-350 / 350)

	time_stamp=time.time()
 	msg = json.JSONEncoder().encode({"d":{"measured_timestamp":time_stamp, "accel_xout_scaled":accel_xout_scaled, "accel_yout_scaled":accel_yout_scaled, "accel_zout_scaled":accel_zout_scaled}})
 
 	mqttc.publish(topic, payload=msg, qos=1, retain=False)
 	print "message published ", time_stamp 

 	time.sleep(0.01)
 	pass

