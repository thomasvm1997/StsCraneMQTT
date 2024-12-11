import time
import json
import paho.mqtt.client as paho
import ssl  # Import ssl module for TLS support
from enum import IntEnum, Enum

# Define enumerations for actions (numeric values)
class GantryAction(IntEnum):
    NEUTRAL = 0
    RIGHT = 1
    LEFT = 2

class HoistAction(IntEnum):
    NEUTRAL = 0
    UP = 1
    DOWN = 2

class TrolleyAction(IntEnum):
    NEUTRAL = 0
    FORWARD = 1
    BACKWARD = 2

class SpreaderAction(IntEnum):
    NEUTRAL = 0
    OPEN = 1
    CLOSE = 2

class HandbrakeAction(IntEnum):
    LOCK = 0
    RELEASE = 1

class EmergencyAction(IntEnum):
    LOCK = 0
    UNLOCK = 1

# Define the SpreaderMovement Enum and Spreader class
class SpreaderMovement(Enum):
    OPEN = 0
    CLOSE = 1
    NEUTRAL = 2

class BaseCraneObject:
    def __init__(self):
        self._increment = 0.2  # Default value

    @property
    def increment(self):
        return self._increment

    @increment.setter
    def increment(self, value):
        if value <= 0.2:
            self._increment = 0.2
        elif value >= 2.0:
            self._increment = 2.0
        else:
            self._increment = value

class Spreader(BaseCraneObject):
    def __init__(self):
        super().__init__()
        self._width = 6.06  # Default value
        self.spreader_movement = SpreaderMovement.NEUTRAL  # Default movement
        self.is_locked = False  # Default lock state

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value >= 14.0:
            self._width = 14.0
        elif value <= 6.06:
            self._width = 6.06
        else:
            self._width = value


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
    "/joysticks/spreader/open",
    "/joysticks/spreader/close",
    "/joysticks/spreader/neutral",
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
    "/joysticks/spreader/open": "/hub/spreader/open",
    "/joysticks/spreader/close": "/hub/spreader/close",
    "/joysticks/spreader/neutral": "/hub/spreader/neutral",
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
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    
    try:
        payload = json.loads(msg.payload)
        component = payload.get('component')
        state = payload.get('state')

        if component and state is not None:
            print(f"Processed action: {component} -> {state}")

            # Map the state to the correct IntEnum class
            action_enum = None
            if component == "gantry":
                action_enum = GantryAction
            elif component == "hoist":
                action_enum = HoistAction
            elif component == "trolley":
                action_enum = TrolleyAction
            elif component == "spreader":
                action_enum = SpreaderAction
            elif component == "handbrake":
                action_enum = HandbrakeAction
            elif component == "emergency":
                action_enum = EmergencyAction

            if action_enum:
                # Convert the state to the corresponding IntEnum value
                try:
                    int_value = action_enum[state.upper()].value  # Ensure state is converted to the corresponding enum
                    # If it's the spreader and movement is neutral, send the custom payload
                    if component == "spreader" and state.lower() == "neutral":
                        spreader = Spreader()  
                        spreader.increment = 0.2
                        spreader.width = 6.06 
                        spreader.spreader_movement = SpreaderMovement.NEUTRAL  # Neutral state
                        spreader.is_locked = False  # Lock state

                        # Create a dictionary for the payload
                        payload_data = {
                            "increment": spreader.increment,
                            "width": spreader.width,
                            "spreader_movement": spreader.spreader_movement.value,  # Enum value (NEUTRAL = 2)
                            "is_locked": spreader.is_locked
                        }

                        # Publish the payload to the spreader neutral topic
                        publish_topic = PUBLISH_TOPICS.get("/joysticks/spreader/neutral")
                        if publish_topic:
                            client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                            print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")
                    else:
                        # For other states, just forward the integer value as normal
                        publish_topic = PUBLISH_TOPICS.get(msg.topic)
                        if publish_topic:
                            client.publish(publish_topic, payload=json.dumps(int_value), qos=1)
                            print(f"Forwarded to {publish_topic} with payload: {int_value}")
                        else:
                            print(f"Invalid topic: {msg.topic}")
                except KeyError:
                    print(f"Invalid state {state} for component {component}")
            else:
                print(f"Unknown component: {component}")

        else:
            print(f"Invalid payload received: {msg.payload.decode()}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Initialize MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# Set TLS configuration
client.tls_set_context(ssl.create_default_context())
client.username_pw_set("shark", "FishFish1")

# Connect to the MQTT broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start the loop
client.loop_start()

try:
    while True:
        time.sleep(1)  # Keep the hub running
except KeyboardInterrupt:
    print("Hub interrupted by user.")
finally:
    client.loop_stop()
    client.disconnect()
    print("MQTT client disconnected.")
