import time
import json
import paho.mqtt.client as paho
from paho import mqtt
import keyboard  # Detects key presses

# Joystick action topics based on the provided list
JOYSTICK_TOPICS = {
    "gantry_left": "/joysticks/gantry/left",
    "gantry_right": "/joysticks/gantry/right",
    "gantry_handbrake_lock": "/joysticks/gantry/handbrake/lock",
    "gantry_handbrake_release": "/joysticks/gantry/handbrake/release",
    "hoist_up": "/joysticks/hoist/up",
    "hoist_down": "/joysticks/hoist/down",
    "trolley_forward": "/joysticks/trolley/forward",
    "trolley_backward": "/joysticks/trolley/backward",
    "spreader_widen": "/joysticks/spreader/widen",
    "spreader_narrow": "/joysticks/spreader/narrow",
    "spreader_lock": "/joysticks/spreader/lock",
    "spreader_unlock": "/joysticks/spreader/unlock",
    "emergency_lock": "/joysticks/emergency/lock",
    "emergency_unlock": "/joysticks/emergency/unlock"
}

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully!")
    else:
        print(f"Failed to connect, return code: {rc}")

# Callback for publish confirmation
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
    print(f"Message published successfully - MID: {mid}")

# Main function to handle joystick key presses and send MQTT messages
def joystick_controller(client):
    print("Joystick control activated. Press 'q' to quit.")
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

            # Avoid high CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Joystick control interrupted.")

    finally:
        client.loop_stop()
        client.disconnect()
        print("MQTT client disconnected.")

# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Set MQTT callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Enable TLS for secure connection
client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)

# Set MQTT username and password
client.username_pw_set("shark", "FishFish1")

# Connect to the HiveMQ broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start the MQTT client loop in the background
client.loop_start()

# Run the joystick check method
check_joysticks(client)