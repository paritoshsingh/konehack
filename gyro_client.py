import time
import paho.mqtt.client as mqtt
import json
import uuid
import smbus
import math
from datetime import datetime


# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)



#Set the variables for connecting to the iot service
broker = ""
deviceId="gyro-pi1" #you can give the 	 address as default also
topic = "iot-2/evt/status/fmt/json"
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
	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)

	gyro_xout_scaled =(gyro_xout / 131)
	gyro_yout_scaled =(gyro_yout / 131)
	gyro_zout_scaled =(gyro_zout / 131)

	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)
	accel_xout_scaled = accel_xout / 16384.0
	accel_yout_scaled = accel_yout / 16384.0
	accel_zout_scaled = accel_zout / 16384.0

	x_rotation=get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	y_rotation=get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	ktime_stamp=time.time()
 	msg = json.JSONEncoder().encode({"d":{"measured_timestamp":time_stamp, "gyro_xout_scaled":gyro_xout_scaled, "gyro_yout_scaled":gyro_yout_scaled, "gyro_zout_scaled":gyro_zout_scaled, "accel_xout_scaled":accel_xout_scaled, "accel_yout_scaled":accel_yout_scaled, "accel_zout_scaled":accel_zout_scaled, "x_rotation":x_rotation, "y_rotation":y_rotation}})
 
 	mqttc.publish(topic, payload=msg, qos=1, retain=False)
 	print "message published ", time_stamp 

 	time.sleep(0.05)
 	pass

