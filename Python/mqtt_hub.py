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
    OPEN = 1
    CLOSE = 2
    NEUTRAL = 0

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
    "/joysticks/spreader/lock",   # New topic for lock
    "/joysticks/spreader/unlock"   # New topic for unlock
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
    "/joysticks/spreader/lock": "/hub/spreader/lock",   # Handle lock
    "/joysticks/spreader/unlock": "/hub/spreader/unlock"   # Handle unlock
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
# Callback for receiving messages
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    try:
        payload = json.loads(msg.payload)
        component = payload.get('component')
        state = payload.get('state')

        if component and state is not None:
            print(f"Processed action: {component} -> {state}")

            # Handle spreader lock/unlock separately
            if component == "spreader":
                if state == "lock":
                    # Lock the spreader and persist the lock state
                    if not hub_spreader.is_locked:  # Only lock if it's not already locked
                        spreader_movement = SpreaderMovement.NEUTRAL
                        payload_data = {
                            "Increment": 0.2,  # Always include increment value
                            "IsLocked": True,   # Lock the spreader
                            "SpreaderMovement": spreader_movement.value,
                            "movement": "neutral"
                        }
                        # Persist the locked state in memory
                        hub_spreader.is_locked = True
                        print("Spreader is locked.")

                    else:
                        print("Spreader is already locked, no action taken.")
                    
                elif state == "unlock":
                    # Unlock the spreader and persist the unlock state
                    if hub_spreader.is_locked:  # Only unlock if it's already locked
                        spreader_movement = SpreaderMovement.NEUTRAL
                        payload_data = {
                            "Increment": 0.2,  # Always include increment value
                            "IsLocked": False,  # Unlock the spreader
                            "SpreaderMovement": spreader_movement.value,
                            "movement": "neutral"
                        }
                        # Persist the unlocked state in memory
                        hub_spreader.is_locked = False
                        print("Spreader is unlocked.")
                    else:
                        print("Spreader is already unlocked, no action taken.")
                
                else:
                    # Handle other spreader movements (open/close)
                    if state.lower() == "open":
                        spreader_movement = SpreaderMovement.OPEN
                        movement_value = "right"
                    elif state.lower() == "close":
                        spreader_movement = SpreaderMovement.CLOSE
                        movement_value = "left"
                    else:
                        spreader_movement = SpreaderMovement.NEUTRAL
                        movement_value = "neutral"

                    payload_data = {
                        "Increment": 0.2,
                        "IsLocked": hub_spreader.is_locked,  # Keep lock state persistent
                        "SpreaderMovement": spreader_movement.value,
                        "movement": movement_value
                    }

                # Publish the payload to the correct topic
                publish_topic = PUBLISH_TOPICS.get(msg.topic)
                if publish_topic:
                    client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                    print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")
            else:
                # For other components (gantry, hoist, etc.)
                action_enum = None
                if component == "gantry":
                    action_enum = GantryAction
                elif component == "hoist":
                    action_enum = HoistAction
                elif component == "trolley":
                    action_enum = TrolleyAction
                elif component == "handbrake":
                    action_enum = HandbrakeAction
                elif component == "emergency":
                    action_enum = EmergencyAction

                if action_enum:
                    int_value = action_enum[state.upper()].value
                    payload_data = {
                        "increment": 0.2,  # Always include increment value
                        "is_locked": hub_spreader.is_locked,  # Always include is_locked value
                        "state": int_value
                    }
                    publish_topic = PUBLISH_TOPICS.get(msg.topic)
                    if publish_topic:
                        client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                        print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")

    except Exception as e:
        print(f"Error: {str(e)}")


# Initialize MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# Create a Spreader instance to track the lock state
hub_spreader = Spreader()

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
