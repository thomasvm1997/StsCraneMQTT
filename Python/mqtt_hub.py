import time
import paho.mqtt.client as paho
from paho import mqtt

# Mapping subscription topics to their respective mapped names
TOPIC_MAPPING = {
    "/joystick/gantry": "/hub/joystick/gantry",
    "/joystick/hoist": "/hub/joystick/hoist",
    "/joystick/trolley": "/hub/joystick/trolley",
    "/joystick/emergency-stop": "/hub/joystick/emergency-stop",
    "/joystick/handbrake": "/hub/joystick/handbrake"
}

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    # Subscribe only to the mapped topics
    for topic in TOPIC_MAPPING.keys():
        client.subscribe(topic, qos=1)
        print(f"Subscribed to {topic}")

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.topic in TOPIC_MAPPING:
        print(f"Message received from mapped topic: {msg.topic}")
    else:
        print(f"Received message from unknown topic: {msg.topic}")

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Set callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# Enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# Set username and password
client.username_pw_set("shark", "FishFish1")

# Connect to HiveMQ broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Run the client loop
client.loop_forever()
