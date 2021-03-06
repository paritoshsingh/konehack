import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import uuid
from datetime import datetime
import sqlite3

#Set the variables for connecting to the iot service
msg= ""
broker = ""
r = []
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
conn=sqlite3.connect("/home/pi/sqlite3/msgDb.db")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    try:
	c = conn.cursor()
	#c.execute("select a.* from messages a left join sent_messages b on a.message_id=b.message_id and b.message_id is null order by a.message_id asc limit 1;")
	c.execute("select * from messages limit 1")
	r = [dict((c.description[i][0], value) \
		for i, value in enumerate(row)) for row in c.fetchall()]
	print "RRR"
	print r[0]		
	# print json.dumps(r[0])	
 	msg = json.JSONEncoder().encode({"d":r[0]})
    except Exception as e:
 	print e
 	conn.close()

def on_publish(mosq, obj, mid):
	print "looking "
	print mid
	try:	
	    c=conn.cursor()
	    c.execute("delete from messages where message_id =(select message_id from sent_messages where mid=?);", mid)
	    c.commit()
	except Exception as e:
	    print e
	    conn.close()
 	print "sent"

##Assign callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

#Set authentication values, if connecting to registered service
if username is not "":
	mqttc.username_pw_set(username, password=password)

mqttc.connect(host=broker, port=1883, keepalive=60)

#Publishing to IBM Internet of Things Foundation
mqttc.loop_start() 

try:
    pub=mqttc.publish(topic, payload=msg, qos=1, retain=False)
    print "mid pubbed"
    print pub.mid
    c=conn.cursor()
    c.execute("insert into sent_messages (message_id, mid) values (?,?)", (1,pub['mid']))
except Exception as e:
    print e	
mqttc.loop_forever()
 	# print "message published"
 	# publish.multiple(r, hostname=broker, port=1883, client_id=clientID, keepalive=60)


