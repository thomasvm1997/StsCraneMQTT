import time
import paho.mqtt.client as paho
import keyboard
import json

# Topics for joystick actions
JOYSTICK_TOPICS = {
    "gantry_left": "/joysticks/gantry/left",
    "gantry_right": "/joysticks/gantry/right",
    "gantry_neutral": "/joysticks/gantry/neutral",
    "hoist_up": "/joysticks/hoist/up",
    "hoist_down": "/joysticks/hoist/down",
    "hoist_neutral": "/joysticks/hoist/neutral",
    "trolley_forward": "/joysticks/trolley/forward",
    "trolley_backward": "/joysticks/trolley/backward",
    "trolley_neutral": "/joysticks/trolley/neutral",
    "handbrake_lock": "/joysticks/gantry/handbrake/lock",
    "handbrake_release": "/joysticks/gantry/handbrake/release",
    "emergency_lock": "/joysticks/emergency/lock",
    "emergency_unlock": "/joysticks/emergency/unlock",
    "spreader_open": "/joysticks/spreader/open",
    "spreader_close": "/joysticks/spreader/close",
    "spreader_neutral": "/joysticks/spreader/neutral",
}

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully!")
    else:
        print(f"Failed to connect, return code: {rc}")

# Callback for publish confirmation
def on_publish(client, userdata, mid, properties=None):
    print(f"Message published successfully - MID: {mid}")

# Function to send joystick states
def send_joystick_states(client):
    joystick_states = {
        "gantry": "neutral",
        "hoist": "neutral",
        "trolley": "neutral",
        "handbrake": "release",
        "emergency": "unlock",
        "spreader": "neutral"
    }

    # Gantry input
    if keyboard.is_pressed('a'):
        joystick_states["gantry"] = "left"
    elif keyboard.is_pressed('d'):
        joystick_states["gantry"] = "right"
    else:
        joystick_states["gantry"] = "neutral"

    # Hoist input
    if keyboard.is_pressed('w'):
        joystick_states["hoist"] = "up"
    elif keyboard.is_pressed('s'):
        joystick_states["hoist"] = "down"
    else:
        joystick_states["hoist"] = "neutral"

    # Trolley input
    if keyboard.is_pressed('i'):
        joystick_states["trolley"] = "forward"
    elif keyboard.is_pressed('k'):
        joystick_states["trolley"] = "backward"
    else:
        joystick_states["trolley"] = "neutral"

    # Spreader input
    if keyboard.is_pressed('o'):
        joystick_states["spreader"] = "open"
    elif keyboard.is_pressed('c'):
        joystick_states["spreader"] = "close"
    else:
        joystick_states["spreader"] = "neutral"

    # Handbrake input
    if keyboard.is_pressed('1'):
        joystick_states["handbrake"] = "lock"
    else:
        joystick_states["handbrake"] = "release"

    # Emergency input
    if keyboard.is_pressed('z'):
        joystick_states["emergency"] = "lock"
    else:
        joystick_states["emergency"] = "unlock"

    # Publish each state and print the result
    for component, state in joystick_states.items():
        if component == "spreader":
            if state == "open":
                topic = JOYSTICK_TOPICS["spreader_open"]
                payload = json.dumps({"component": component, "state": "open"})
            elif state == "close":
                topic = JOYSTICK_TOPICS["spreader_close"]
                payload = json.dumps({"component": component, "state": "close"})
            else:
                topic = JOYSTICK_TOPICS["spreader_neutral"]
                payload = json.dumps({"component": component, "state": "neutral"})
        else:
            topic = JOYSTICK_TOPICS.get(f"{component}_{state}")
            payload = json.dumps({"component": component, "state": state})
        
        if topic:
            client.publish(topic, payload, qos=1)
            print(f"Published to {topic}: {payload}")

# Initialize MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_publish = on_publish

# Enable TLS for secure connection
client.tls_set()
client.username_pw_set("shark", "FishFish1")

# Connect to the broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start the MQTT client loop in the background
client.loop_start()

try:
    print("Joystick control activated. Press 'q' to quit.")
    while True:
        send_joystick_states(client)
        time.sleep(1)  # Check every second
        if keyboard.is_pressed('q'):
            print("Exiting joystick control...")
            break
except KeyboardInterrupt:
    print("Joystick control interrupted.")
finally:
    client.loop_stop()
    client.disconnect()
    print("MQTT client disconnected.")
