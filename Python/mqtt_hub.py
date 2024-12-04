import time
import paho.mqtt.client as paho
from paho import mqtt

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
    "/joysticks/spreader/open",
    "/joysticks/spreader/close",
    "/joysticks/spreader/lock",
    "/joysticks/spreader/unlock",
    "/spreader/status/open",
    "/spreader/status/closed",
    "/spreader/status/locked",
    "/spreader/status/unlocked",
    # Emergency
    "/joysticks/emergency/lock",
    "/joysticks/emergency/unlock"
]

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
    "/joysticks/spreader/open": "/hub/spreader/open",
    "/joysticks/spreader/close": "/hub/spreader/close",
    "/joysticks/spreader/lock": "/hub/spreader/lock",
    "/joysticks/spreader/unlock": "/hub/spreader/unlock",
    "/spreader/status/open": "/hub/spreader/status/open",
    "/spreader/status/closed": "/hub/spreader/status/closed",
    "/spreader/status/locked": "/hub/spreader/status/locked",
    "/spreader/status/unlocked": "/hub/spreader/status/unlocked",
    # Emergency
    "/joysticks/emergency/lock": "/hub/emergency/lock",
    "/joysticks/emergency/unlock": "/hub/emergency/unlock"
}

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    # Subscribe to all topics in SUBSCRIPTIONS
    for topic in SUBSCRIPTIONS:
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

    # Check if the topic should be published elsewhere
    if msg.topic in PUBLISH_TOPICS:
        target_topic = PUBLISH_TOPICS[msg.topic]
        client.publish(target_topic, payload=msg.payload, qos=1)
        print(f"Forwarded message from {msg.topic} to {target_topic}")

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
