import time
import json
import paho.mqtt.client as paho
from paho import mqtt
from enum import Enum

# Define enumerations for actions
class GantryAction(Enum):
    LEFT = "left"
    RIGHT = "right"
    NEUTRAL = "neutral"

class HoistAction(Enum):
    UP = "up"
    DOWN = "down"
    NEUTRAL = "neutral"

class TrolleyAction(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    NEUTRAL = "neutral"

class HandbrakeAction(Enum):
    LOCK = "lock"
    RELEASE = "release"

class EmergencyAction(Enum):
    LOCK = "lock"
    UNLOCK = "unlock"

# List of topics the Hub subscribes to
SUBSCRIPTIONS = [
    "/joysticks/gantry/left",
    "/joysticks/gantry/right",
    "/joysticks/gantry/neutral",
    "/joysticks/hoist/up",
    "/joysticks/hoist/down",
    "/joysticks/hoist/neutral",
    "/joysticks/trolley/forward",
    "/joysticks/trolley/backward",
    "/joysticks/trolley/neutral",
    "/joysticks/gantry/handbrake/lock",
    "/joysticks/gantry/handbrake/release",
    "/joysticks/emergency/lock",
    "/joysticks/emergency/unlock",
]

# Map incoming topics to their corresponding Hub publication topics
PUBLISH_TOPICS = {
    "/joysticks/gantry/left": "/hub/gantry/left",
    "/joysticks/gantry/right": "/hub/gantry/right",
    "/joysticks/gantry/neutral": "/hub/gantry/neutral",
    "/joysticks/hoist/up": "/hub/hoist/up",
    "/joysticks/hoist/down": "/hub/hoist/down",
    "/joysticks/hoist/neutral": "/hub/hoist/neutral",
    "/joysticks/trolley/forward": "/hub/trolley/forward",
    "/joysticks/trolley/backward": "/hub/trolley/backward",
    "/joysticks/trolley/neutral": "/hub/trolley/neutral",
    "/joysticks/gantry/handbrake/lock": "/hub/gantry/handbrake/lock",
    "/joysticks/gantry/handbrake/release": "/hub/gantry/handbrake/release",
    "/joysticks/emergency/lock": "/hub/emergency/lock",
    "/joysticks/emergency/unlock": "/hub/emergency/unlock",
}

# Callback for successful connection
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"CONNACK received with code {rc}.")
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
        payload = msg.payload.decode("utf-8")
        action_enum = None

        # Determine the action enum based on the topic
        if msg.topic.startswith("/joysticks/gantry"):
            action_enum = GantryAction(payload)
        elif msg.topic.startswith("/joysticks/hoist"):
            action_enum = HoistAction(payload)
        elif msg.topic.startswith("/joysticks/trolley"):
            action_enum = TrolleyAction(payload)
        elif msg.topic.startswith("/joysticks/gantry/handbrake"):
            action_enum = HandbrakeAction(payload)
        elif msg.topic.startswith("/joysticks/emergency"):
            action_enum = EmergencyAction(payload)

        # Log the action enum
        if action_enum:
            print(f"Processed action: {action_enum}")

        # Forward to the appropriate topic
        if msg.topic in PUBLISH_TOPICS:
            target_topic = PUBLISH_TOPICS[msg.topic]
            client.publish(target_topic, payload=json.dumps({"action": payload}), qos=1)
            print(f"Forwarded to {target_topic} with payload: {payload}")

        # Also forward all messages to /hub/client
        client.publish("/hub/client", payload=json.dumps({"topic": msg.topic, "action": payload}), qos=1)
        print(f"Forwarded to /hub/client: {msg.topic}, payload: {payload}")

    except ValueError as e:
        print(f"Invalid action or topic: {e}")

# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# Enable TLS for secure connection
client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)
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
