import time
import json
import paho.mqtt.client as paho
from paho import mqtt

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Client connected successfully to broker.")

        client.subscribe("/hub/client", qos=1)
        print("Subscribed to /hub/client.")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback for successful publish
def on_publish(client, userdata, mid, properties=None):
    print(f"Message published successfully with MID: {mid}")

# Callback for subscription success
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed successfully - MID: {mid}, QoS: {granted_qos}")

# Callback for receiving messages
def on_message(client, userdata, msg):
    print(f"Client received message - Topic: {msg.topic}, Payload: {msg.payload.decode('utf-8')}")
    try:
        # Convert the payload to a JSON object
        json_object = json.loads(msg.payload.decode('utf-8'))
        print("JSON object:", json_object)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Assign callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# Enable TLS for secure connection
client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)

# Set username and password for MQTT
client.username_pw_set("shark", "FishFish1")

# Connect to HiveMQ broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start the MQTT loop in the background
client.loop_start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()