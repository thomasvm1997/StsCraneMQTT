import time
import json
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
    try:
        # Omzetten van de payload naar een JSON-object
        json_object = json.loads(msg.payload.decode('utf-8'))
        print(json_object)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

# Main method to check joystick key presses and send messages
def check_joysticks(client):
    print("Controlling joysticks. Press 'q' to quit.")
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Exiting joystick control...")
                break

            # Gantry joystick
            if keyboard.is_pressed('w'):  # Move gantry forward
                payload = json.dumps({"action": "joystick gantry forward"})
                client.publish("/joystick/gantry", payload=payload, qos=1)
                print("Gantry joystick forward")
                time.sleep(0.3)
            elif keyboard.is_pressed('e'):  # Move gantry backward
                payload = json.dumps({"action": "joystick gantry backward"})
                client.publish("/joystick/gantry", payload=payload, qos=1)
                print("Gantry joystick backward")
                time.sleep(0.3)

            elif keyboard.is_pressed('5'):  # Emergency stop for gantry
                payload = json.dumps({"action": "emergency stop activated"})
                client.publish("/joystick/emergency-stop", payload=payload, qos=1)
                print("Emergency stop activated")
                time.sleep(0.3)

            # Trolley joystick
            if keyboard.is_pressed('s'):  # Move trolley left
                payload = json.dumps({"action": "joystick trolley left"})
                client.publish("/joystick/trolley", payload=payload, qos=1)
                print("Trolley joystick left")
                time.sleep(0.3)
            elif keyboard.is_pressed('d'):  # Move trolley right
                payload = json.dumps({"action": "joystick trolley right"})
                client.publish("/joystick/trolley", payload=payload, qos=1)
                print("Trolley joystick right")
                time.sleep(0.3)

            # Hoist joystick
            if keyboard.is_pressed('x'):  # Move hoist up
                payload = json.dumps({"action": "joystick hoist up"})
                client.publish("/joystick/hoist", payload=payload, qos=1)
                print("Hoist joystick up")
                time.sleep(0.3)
            elif keyboard.is_pressed('c'):  # Move hoist down
                payload = json.dumps({"action": "joystick hoist down"})
                client.publish("/joystick/hoist", payload=payload, qos=1)
                print("Hoist joystick down")
                time.sleep(0.3)

            # Handbrake
            if keyboard.is_pressed('4'):
                payload = json.dumps({"action": "handbrake active"})
                client.publish("/joystick/handbrake", payload=payload, qos=1)
                print("Handbrake active")
                time.sleep(0.3)        

            elif keyboard.is_pressed('6'):  # spreader
                payload = json.dumps({"action": "spreader activated"})
                client.publish("/joystick/spreader", payload=payload, qos=1)
                print("Spreader activated")
                time.sleep(0.3)
            
            elif keyboard.is_pressed('7'):  # spreader lock
                payload = json.dumps({"action": "spreader lock activated"})
                client.publish("/joystick/spreader", payload=payload, qos=1)
                print("Spreader lock activated")
                time.sleep(0.3)

        else:
            # No key pressed, no action
            time.sleep(0.1)  # Sleep for a small time to avoid high CPU usage
    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        client.loop_stop()
        client.disconnect()

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

# Run the joystick check method
check_joysticks(client)