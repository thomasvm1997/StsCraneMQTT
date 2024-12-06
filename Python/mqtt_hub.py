import time
import json
import paho.mqtt.client as paho
from paho import mqtt

# List of topics the Hub subscribes to
SUBSCRIPTIONS = [
    # Gantry
    "/joysticks/gantry/left",
    "/joysticks/gantry/right",
    "/joysticks/gantry/handbrake/lock",
    "/joysticks/gantry/handbrake/release",
    "/gantry/location",
    # Hoist
    "/joysticks/hoist/up",
    "/joysticks/hoist/down",
    "/hoist/location",
    # Trolley
    "/joysticks/trolley/forward",
    "/joysticks/trolley/backward",
    "/trolley/location",
    # Spreader
    "/joysticks/spreader/widen",
    "/joysticks/spreader/narrow",
    "/joysticks/spreader/lock",
    "/joysticks/spreader/unlock",
    "/spreader/widen",
    "/spreader/narrow",
    "/spreader/lock",
    "/spreader/unlock",
    # Emergency Button
    "/joysticks/emergency/lock",
    "/joysticks/emergency/unlock"
]

# Map incoming topics to their corresponding Hub publication topics
PUBLISH_TOPICS = {
    # Gantry
    "/joysticks/gantry/left": "/hub/gantry/left",
    "/joysticks/gantry/right": "/hub/gantry/right",
    "/joysticks/gantry/handbrake/lock": "/hub/gantry/handbrake/lock",
    "/joysticks/gantry/handbrake/release": "/hub/gantry/handbrake/release",
    "/gantry/location": "/hub/gantry/location",
    # Hoist
    "/joysticks/hoist/up": "/hub/hoist/up",
    "/joysticks/hoist/down": "/hub/hoist/down",
    "/hoist/location": "/hub/hoist/location",
    # Trolley
    "/joysticks/trolley/forward": "/hub/trolley/forward",
    "/joysticks/trolley/backward": "/hub/trolley/backward",
    "/trolley/location": "/hub/trolley/location",
    # Spreader
    "/joysticks/spreader/widen": "/hub/spreader/widen",
    "/joysticks/spreader/narrow": "/hub/spreader/narrow",
    "/joysticks/spreader/lock": "/hub/spreader/lock",
    "/joysticks/spreader/unlock": "/hub/spreader/unlock",
    "/spreader/widen": "/hub/spreader/widen",
    "/spreader/narrow": "/hub/spreader/narrow",
    "/spreader/lock": "/hub/spreader/lock",
    "/spreader/unlock": "/hub/spreader/unlock",
    # Emergency Button
    "/joysticks/emergency/lock": "/hub/emergency/lock",
    "/joysticks/emergency/unlock": "/hub/emergency/unlock"
}

# Callback for successful connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    # Subscribe to all topics
    for topic in SUBSCRIPTIONS:
        client.subscribe(topic, qos=1)
        print(f"Subscribed to {topic}")

# Callback for successful publish
def on_publish(client, userdata, mid, properties=None):
    print(f"Message published with mid: {mid}")

# Callback for subscription confirmation
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed: mid={mid}, qos={granted_qos}")

# Callback for receiving messages
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")
    
    try:
        # Omzetten van de payload naar een JSON-object
        json_object = json.loads(msg.payload.decode('utf-8'))
        print("JSON object:", json_object)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return

    # Check if the topic has a mapped publication topic
    if msg.topic in PUBLISH_TOPICS:
        target_topic = PUBLISH_TOPICS[msg.topic]
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
