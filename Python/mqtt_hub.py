import time
import json
import paho.mqtt.client as paho
from paho import mqtt

# Mapping subscription topics to their respective mapped names
TOPIC_MAPPING = {
    "/joystick/gantry": "/hub/joystick/gantry",
    "/joystick/hoist": "/hub/joystick/hoist",
    "/joystick/trolley": "/hub/joystick/trolley",
    "/joystick/emergency-stop": "/hub/joystick/emergency-stop",
    "/joystick/handbrake": "/hub/joystick/handbrake",
    "/spreader": "/hub/spreader",
    "spreader/lock": "/hub/spreader/lock",
    "spreader/unlock": "/hub/spreader/unlock",
    "/gantry": "/hub/gantry",
    "/trolley": "/hub/trolley",
    "/hoist": "/hub/hoist",
    "/client": "/hub/client"
}

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    # Subscribe to all topics in TOPIC_MAPPING
    for topic in TOPIC_MAPPING.keys():
        client.subscribe(topic, qos=1)
        print(f"Subscribed to {topic}")

# Callback for successful publish
def on_publish(client, userdata, mid, properties=None):
    print("Message published with mid: " + str(mid))

# Callback for subscription confirmation
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Callback for receiving messages
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {str(msg.payload.decode('utf-8'))}")
    try:
        # Omzetten van de payload naar een JSON-object
        json_object = json.loads(msg.payload.decode('utf-8'))
        print("JSON object:", json_object)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return

    # Forward the message to the mapped topic
    if msg.topic in TOPIC_MAPPING:
        target_topic = TOPIC_MAPPING[msg.topic]
        client.publish(target_topic, payload=json.dumps(json_object), qos=1)
        print(f"Forwarded message from {msg.topic} to {target_topic} with payload: {json.dumps(json_object)}")

    # Forward every message to /hub/client
    client.publish("/hub/client", payload=json.dumps(json_object), qos=1)
    print(f"Forwarded message from {msg.topic} to /hub/client with payload: {json.dumps(json_object)}")


# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Set callbacks
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