import time
import paho.mqtt.client as mqtt
import json
import uuid


#Class for retrieving CPU % utilisation
class CPUutil(object):
 def __init__(self):
 	self.prev_idle = 0
 	self.prev_total = 0
 	self.new_idle = 0
 	self.new_total = 0
def get(self):
	self.read()
	delta_idle = self.new_idle - self.prev_idle
	delta_total = self.new_total - self.prev_total
	cpuut = 0.0
	if (self.prev_total != 0) and (delta_total != 0):
		cpuut = ((delta_total - delta_idle) * 100.0 / delta_total)
		return cpuut
def read(self):
	self.prev_idle = self.new_idle
	self.prev_total = self.new_total
	self.new_idle = 0;
	self.new_total = 0;
with open('/proc/stat') as f:
	line = f.readline()
	parts = line.split()
	if len(parts) >= 5:
	self.new_idle = int(parts[4])
	for part in parts[1:]:
	self.new_total += int(part)


#Initialise class to retrieve CPU Usage
cpuutil = CPUutil()

macAddress = hex(uuid.getnode())[2:-1]macAddress = format(long(macAddress, 16),'012x')
#macAddress="0017c4a5db29" #you can give the mac address as default also

#Set the variables for connecting to the iot service
broker = ""
topic = "iot-2/evt/status/fmt/json"
username = "use-token-auth"
password = "gyropiauth" #auth-token
organization = "blve66" #org_id
deviceType = "gyro-pi"

topic = "iot-2/evt/status/fmt/json"


print("MAC address: " + macAddress)


#Creating the client connection
#Set clientID and broker
clientID = "aaaaa:" + organization + ":" + deviceType + ":" + macAddress
broker = organization + ".messaging.internetofthings.ibmcloud.com"
mqttc = mqtt.Client(clientID)

#Set authentication values, if connecting to registered service
if username is not "":
	mqttc.username_pw_set(username, password=password)

mqttc.connect(host=broker, port=1883, keepalive=60)


#Publishing to IBM Internet of Things Foundation
mqttc.loop_start() 

while mqttc.loop() == 0:
	cpuutilvalue = cpuutil.get()
 	print cpuutilvalue

 	msg = json.JSONEncoder().encode({"aaaa":{"cpuutil":cpuutilvalue}})
 
 	mqttc.publish(topic, payload=msg, qos=0, retain=False)
 	print "message published"

 	time.sleep(5)
 	pass

