import time
import json
import paho.mqtt.client as paho
from paho import mqtt
from trolley_object import Trolley

trolley = Trolley(x=100, y=300, width=50, height=20, min_x=50, max_x=750)

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    client.subscribe("/hub/trolley", qos=1)
    print("Subscribed to hub/trolley")

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload)) #message content
    try:
        payload = json.loads(msg.payload.decode()) 
        if msg.topic == "/hub/trolley":
            if "command" in payload:
                command = payload["command"]
                if command == "move":
                    direction = int(payload["direction"]) #-1 left, 1 right
                    delta_time = time.time() - trolley.last_update #calculates time elapsed since last update
                    trolley.move(direction, delta_time) #update position
                elif command == "speed":
                    trolley.set_speed(float(payload["speed"])) #sets speed
                elif command == "stop":
                    trolley.emergency_stop_action() #activates emergency stop
                elif command == "release_stop":
                    trolley.release_emergency_stop() #release emergency stop
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing message: {e}")

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("shark", "FishFish1")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


# a single publish, this can also be done in loops, etc.
client.publish("/trolley", payload= "hot", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()