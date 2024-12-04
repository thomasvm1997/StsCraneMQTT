import time
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
    print(f"Message published successfully - MID: {mid}")

# Main function to handle joystick key presses and send MQTT messages
def joystick_controller(client):
    print("Joystick control activated. Press 'q' to quit.")
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Exiting joystick control...")
                break

            # Gantry actions
            if keyboard.is_pressed('a'):  # Gantry move left
                client.publish(JOYSTICK_TOPICS["gantry_left"], "gantry left", qos=1)
                print("Gantry left")
                time.sleep(0.3)
            elif keyboard.is_pressed('d'):  # Gantry move right
                client.publish(JOYSTICK_TOPICS["gantry_right"], "gantry right", qos=1)
                print("Gantry right")
                time.sleep(0.3)
            elif keyboard.is_pressed('1'):  # Gantry handbrake lock
                client.publish(JOYSTICK_TOPICS["gantry_handbrake_lock"], "handbrake lock", qos=1)
                print("Gantry handbrake lock")
                time.sleep(0.3)
            elif keyboard.is_pressed('2'):  # Gantry handbrake release
                client.publish(JOYSTICK_TOPICS["gantry_handbrake_release"], "handbrake release", qos=1)
                print("Gantry handbrake release")
                time.sleep(0.3)

            # Hoist actions
            if keyboard.is_pressed('w'):  # Hoist up
                client.publish(JOYSTICK_TOPICS["hoist_up"], "hoist up", qos=1)
                print("Hoist up")
                time.sleep(0.3)
            elif keyboard.is_pressed('s'):  # Hoist down
                client.publish(JOYSTICK_TOPICS["hoist_down"], "hoist down", qos=1)
                print("Hoist down")
                time.sleep(0.3)

            # Trolley actions
            if keyboard.is_pressed('i'):  # Trolley forward
                client.publish(JOYSTICK_TOPICS["trolley_forward"], "trolley forward", qos=1)
                print("Trolley forward")
                time.sleep(0.3)
            elif keyboard.is_pressed('k'):  # Trolley backward
                client.publish(JOYSTICK_TOPICS["trolley_backward"], "trolley backward", qos=1)
                print("Trolley backward")
                time.sleep(0.3)

            # Spreader actions
            if keyboard.is_pressed('o'):  # Spreader widen
                client.publish(JOYSTICK_TOPICS["spreader_widen"], "spreader widen", qos=1)
                print("Spreader widen")
                time.sleep(0.3)
            elif keyboard.is_pressed('l'):  # Spreader narrow
                client.publish(JOYSTICK_TOPICS["spreader_narrow"], "spreader narrow", qos=1)
                print("Spreader narrow")
                time.sleep(0.3)
            elif keyboard.is_pressed('p'):  # Spreader lock
                client.publish(JOYSTICK_TOPICS["spreader_lock"], "spreader lock", qos=1)
                print("Spreader lock")
                time.sleep(0.3)
            elif keyboard.is_pressed(';'):  # Spreader unlock
                client.publish(JOYSTICK_TOPICS["spreader_unlock"], "spreader unlock", qos=1)
                print("Spreader unlock")
                time.sleep(0.3)

            # Emergency actions
            if keyboard.is_pressed('z'):  # Emergency lock
                client.publish(JOYSTICK_TOPICS["emergency_lock"], "emergency lock", qos=1)
                print("Emergency lock")
                time.sleep(0.3)
            elif keyboard.is_pressed('x'):  # Emergency unlock
                client.publish(JOYSTICK_TOPICS["emergency_unlock"], "emergency unlock", qos=1)
                print("Emergency unlock")
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

# Enable TLS for secure MQTT connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# Set MQTT username and password
client.username_pw_set("shark", "FishFish1")

# Connect to the HiveMQ broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start the MQTT client loop in the background
client.loop_start()

# Run the joystick controller
joystick_controller(client)
