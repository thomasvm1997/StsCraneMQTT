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

class HoistMovement(Enum):
    NEUTRAL = 0
    UP = 1
    DOWN = 2

class TrolleyMovement(Enum):  # Added Trolley Movement Enum
    NEUTRAL = 0
    FORWARD = 1
    BACKWARD = 2

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
        self._width = 6.06
        self.spreader_movement = SpreaderMovement.NEUTRAL  # Default movement
        self.is_locked = False

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


class Hoist(BaseCraneObject):
    def __init__(self):
        super().__init__()
        self._hight = 0  #
        self.hoist_movement = HoistMovement.NEUTRAL  # Default hoist movement (neutral)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if value <= 0:
            self._length = 0
        elif value >= 100:
            self._length = 100
        else:
            self._length = value

# Trolley class added
class Trolley(BaseCraneObject):
    def __init__(self):
        super().__init__()
        self._length = 0
        self.trolley_movement = TrolleyMovement.NEUTRAL
        
class Gantry(BaseCraneObject):
    def __init__(self):
        super().__init__()
        self._latteral = 0
        self.gantry_action = GantryAction.NEUTRAL  
        self.is_handbrake_locked = False  

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
    "/joysticks/spreader/lock",   
    "/joysticks/spreader/unlock"
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
    "/joysticks/spreader/lock": "/hub/spreader/lock",   
    "/joysticks/spreader/unlock": "/hub/spreader/unlock"
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

            # Handle spreader lock/unlock separately
            if component == "spreader":
                if state == "lock":
                    # Lock the spreader and persist the lock state
                    if not hub_spreader.is_locked:
                        spreader_movement = SpreaderMovement.NEUTRAL
                        payload_data = {
                            "Increment": 0.2,
                            "IsLocked": True,
                            "SpreaderMovement": spreader_movement.value,
                            "movement": "neutral"
                        }
                        hub_spreader.is_locked = True
                        print("Spreader is locked.")
                    else:
                        print("Spreader is already locked, no action taken.")
                    
                elif state == "unlock":
                    if hub_spreader.is_locked:
                        spreader_movement = SpreaderMovement.NEUTRAL
                        payload_data = {
                            "Increment": 0.2,
                            "IsLocked": False,
                            "SpreaderMovement": spreader_movement.value,
                            "movement": "neutral"
                        }
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
                        "IsLocked": hub_spreader.is_locked,
                        "SpreaderMovement": spreader_movement.value,
                        "movement": movement_value
                    }

                publish_topic = PUBLISH_TOPICS.get(msg.topic)
                if publish_topic:
                    client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                    print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")
            
            # Handle hoist actions (up/down/neutral)
            elif component == "hoist":
                if state == "up":
                    hoist_movement = HoistMovement.UP
                    payload_data = {
                        "Increment": 0.2,
                        "HoistMovement": hoist_movement.value,
                        "movement": "up"
                    }
                    print("Hoist moving UP.")
                elif state == "down":
                    hoist_movement = HoistMovement.DOWN
                    payload_data = {
                        "Increment": 0.2,
                        "HoistMovement": hoist_movement.value,
                        "movement": "down"
                    }
                    print("Hoist moving DOWN.")
                else:
                    hoist_movement = HoistMovement.NEUTRAL
                    payload_data = {
                        "Increment": 0.2,
                        "HoistMovement": hoist_movement.value,
                        "movement": "neutral"
                    }
                    print("Hoist is in NEUTRAL.")

                publish_topic = PUBLISH_TOPICS.get(msg.topic)
                if publish_topic:
                    client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                    print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")

            # Handle trolley actions (forward/backward/neutral)
            elif component == "trolley":
                if state == "forward":
                    trolley_movement = TrolleyMovement.FORWARD
                    payload_data = {
                        "Increment": 0.2,
                        "TrolleyMovement": trolley_movement.value,
                        "movement": "forward"
                    }
                    print("Trolley moving FORWARD.")
                elif state == "backward":
                    trolley_movement = TrolleyMovement.BACKWARD
                    payload_data = {
                        "Increment": 0.2,
                        "TrolleyMovement": trolley_movement.value,
                        "movement": "backward"
                    }
                    print("Trolley moving BACKWARD.")
                else:
                    trolley_movement = TrolleyMovement.NEUTRAL
                    payload_data = {
                        "Increment": 0.2,
                        "TrolleyMovement": trolley_movement.value,
                        "movement": "neutral"
                    }
                    print("Trolley is in NEUTRAL.")

                publish_topic = PUBLISH_TOPICS.get(msg.topic)
                if publish_topic:
                    client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                    print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")
            elif component == "gantry":
                if state == "left":
                    if not hub_gantry.is_handbrake_locked:
                        hub_gantry.gantry_action = GantryAction.LEFT
                        print("Gantry moving LEFT.")
                    else:
                        print("Cannot move gantry, handbrake is locked.")
                elif state == "right":
                    if not hub_gantry.is_handbrake_locked:
                        hub_gantry.gantry_action = GantryAction.RIGHT
                        print("Gantry moving RIGHT.")
                    else:
                        print("Cannot move gantry, handbrake is locked.")
                else:  # Neutral or invalid state
                    hub_gantry.gantry_action = GantryAction.NEUTRAL
                    print("Gantry in NEUTRAL.")

                payload_data = {
                    "Increment": 0.2,
                    "GantryAction": hub_gantry.gantry_action.value,
                    "movement": state.lower()
                }

                publish_topic = PUBLISH_TOPICS.get(msg.topic)
                if publish_topic:
                    client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                    print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")

            # Handle handbrake lock and release actions
            elif component == "handbrake":
                if state == "lock":
                    hub_gantry.is_handbrake_locked = True
                    print("Gantry handbrake LOCKED.")
                elif state == "release":
                    hub_gantry.is_handbrake_locked = False
                    print("Gantry handbrake RELEASED.")
                else:
                    print(f"Invalid handbrake state: {state}")

                payload_data = {
                    "Increment": 0.2,
                    "IsHandbrakeLocked": hub_gantry.is_handbrake_locked
                }

                publish_topic = PUBLISH_TOPICS.get(msg.topic)
                if publish_topic:
                    client.publish(publish_topic, payload=json.dumps(payload_data), qos=1)
                    print(f"Forwarded to {publish_topic} with payload: {json.dumps(payload_data)}")

            else:
                # Handle other components like gantry, handbrake, emergency
                action_enum = None
                if component == "gantry":
                    action_enum = GantryAction
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

# Create instances to track the spreader, hoist, and trolley states
hub_spreader = Spreader()
hub_hoist = Hoist()
hub_trolley = Trolley()
hub_gantry = Gantry()  # Initialize Trolley instance

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
