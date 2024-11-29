import time
import paho.mqtt.client as paho
from paho import mqtt
import keyboard  

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
    # Subscribe to /hub/joystick/hoist
    client.subscribe("/hub/joystick/hoist", qos=1)
    print("Subscribed to /hub/joystick/hoist")

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {str(msg.payload.decode('utf-8'))}")

# Method to send message to /joystick/hoist when the '1' key is held down
def hoist_joystick(client):
    while True:
        key_pressed = False
        if keyboard.is_pressed('1'):
            key_pressed = True
            message = "joystick hoist active"
            client.publish("/joystick/hoist", payload=message, qos=1)
            print(f"Sent message to /joystick/hoist: {message}")
            time.sleep(1)
        elif not key_pressed:
            print("Waiting for '1' key press...")


# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Set callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set("shark", "FishFish1")

client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

client.loop_start()

hoist_joystick(client)
