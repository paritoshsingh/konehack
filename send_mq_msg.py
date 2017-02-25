import time
import paho.mqtt.client as mqtt
import json
import uuid
from datetime import datetime
import sqlite3

#Set the variables for connecting to the iot service
broker = ""
deviceId="gyro-pi1" #you can give the 	 address as default also
topic = "iot-2/evt/status/fmt/json"
username = "use-token-auth"
password = "gyropiauth" #auth-token
organization = "blve66" #org_id
deviceType = "gyro-pi"

topic = "iot-2/evt/status/fmt/json"


print("devicid: " + deviceId)


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
	# gyro_xout = read_word_2c(0x43)
	# gyro_yout = read_word_2c(0x45)
	# gyro_zout = read_word_2c(0x47)

	# gyro_xout_scaled =(gyro_xout / 131)
	# gyro_yout_scaled =(gyro_yout / 131)
	# gyro_zout_scaled =(gyro_zout / 131)

	# accel_xout = read_word_2c(0x3b)
	# accel_yout = read_word_2c(0x3d)
	# accel_zout = read_word_2c(0x3f)
	# accel_xout_scaled = accel_xout / 16384.0
	# accel_yout_scaled = accel_yout / 16384.0
	# accel_zout_scaled = accel_zout / 16384.0

	# x_rotation=get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	# y_rotation=get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	try:
		conn=sqlite3.connect("sqlite3/msgDb.db")
		c = conn.cursor()
		c.execute("select a.* from messages a left join sent_messages b on a.message_id=b.message_id and b.message_id is null limit 1;")
		r = [dict((c.description[i][0], value) \
			for i, value in enumerate(row)) for row in c.fetchall()]
		
		print json.dumps(r[0])	
 		msg = json.JSONEncoder().encode({"d":json.dumps(r[0])})
 		json.dumps(msg)
 	except:
 		print "errpr"
 		conn.close()
 	# mqttc.publish(topic, payload=msg, qos=1, retain=False)
 	print "message published"

 	
 	pass

