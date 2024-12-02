import time
import paho.mqtt.client as paho
from paho import mqtt
import keyboard  # Used to detect key presses

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
    # Subscribe to mapped topics
    for topic in TOPIC_MAPPING.values():
        client.subscribe(topic, qos=1)
        print(f"Subscribed to {topic}")

# Callback for publish success
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# Callback for subscription confirmation
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Callback for message receipt
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {str(msg.payload.decode('utf-8'))}")

# Main method to check joystick key presses and send messages
def check_joysticks(client):
    print("Waiting for joystick button presses...")  # Message printed once at the start

    while True:
        if keyboard.is_pressed('1'):  # Hoist joystick
            client.publish("/joystick/hoist", payload="joystick hoist active", qos=1)
            time.sleep(1)  # Send the message every 1 second while the key is pressed

        elif keyboard.is_pressed('2'):  # Trolley joystick
            client.publish("/joystick/trolley", payload="joystick trolley active", qos=1)
            time.sleep(1)

        elif keyboard.is_pressed('3'):  # Gantry joystick
            client.publish("/joystick/gantry", payload="joystick gantry active", qos=1)
            time.sleep(1)

        elif keyboard.is_pressed('4'):  # Handbrake
            client.publish("/joystick/handbrake", payload="handbrake active", qos=1)
            time.sleep(1)

        elif keyboard.is_pressed('5'):  # Emergency stop
            client.publish("/joystick/emergency-stop", payload="emergency stop activated", qos=1)
            time.sleep(1)

        elif keyboard.is_pressed('6'):  # spreader
            client.publish("/joystick/spreader", payload="spreader activated", qos=1)
            time.sleep(1)
        
        elif keyboard.is_pressed('7'):  # spreader lock
            client.publish("/joystick/spreader", payload="spreder lock activated", qos=1)
            time.sleep(1)

        else:
            # No key pressed, no action
            time.sleep(0.1)  # Sleep for a small time to avoid high CPU usage

# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Set callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# Enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# Set username and password for MQTT
client.username_pw_set("shark", "FishFish1")

# Connect to HiveMQ broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start the MQTT loop in the background
client.loop_start()

# Run the joystick check method
check_joysticks(client)
