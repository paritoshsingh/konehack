import time
import paho.mqtt.client as mqtt
import json
import uuid



deviceId="gyro-pi1" #you can give the mac address as default also

#Set the variables for connecting to the iot service
broker = ""
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
	cpuutilvalue = 11
	print cpuutilvalue

 	msg = json.JSONEncoder().encode({"aaaa":{"blah":cpuutilvalue}})
 
 	mqttc.publish(topic, payload=msg, qos=0, retain=False)
 	print "message published"

 	time.sleep(5)
 	pass

