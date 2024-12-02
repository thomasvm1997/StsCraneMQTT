import time
import paho.mqtt.client as paho
from paho import mqtt

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected to broker with CONNACK code: {rc}")
    # Subscribe to all topics using the wildcard "#"
    client.subscribe("hub/#", qos=1)
    print("Subscribed to all topics from hub (hub/#)")

# Callback for successful publish
def on_publish(client, userdata, mid, properties=None):
    print(f"Message published successfully with MID: {mid}")

# Callback for subscription success
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed successfully - MID: {mid}, QoS: {granted_qos}")

# Callback for receiving messages
def on_message(client, userdata, msg):
    print(f"Received message - Topic: {msg.topic}, QoS: {msg.qos}, Payload: {msg.payload.decode('utf-8')}")

# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Assign callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# Set credentials
client.username_pw_set("shark", "FishFish1")

# Connect to the broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Publish a test message
client.publish("test/topic", payload="Hello from MQTT!", qos=1)

# Start the loop
client.loop_forever()
