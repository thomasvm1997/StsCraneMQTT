import time
import json
import paho.mqtt.client as paho
from paho import mqtt
from trolley_object import Trolley, TrolleyMovement


class TrolleyController:
    def __init__(self):
        """Initialize TrolleyController and set up MQTT client."""
        self.trolley = Trolley(x=100, y=300, width=50, height=20, min_x=0, max_x=500)
        self.running = True

        # Initialize MQTT client
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish

        # Set TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set("shark", "FishFish1")
        self.client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

    # MQTT Callbacks
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback for when the MQTT client connects to the broker."""
        print(f"Connected to MQTT broker with code {rc}.")
        client.subscribe("/hub/trolley", qos=1)
        print("Subscribed to /hub/trolley")

    def on_message(self, client, userdata, msg):
        """Callback for receiving messages on subscribed topics."""
        print(f"Message received: {msg.topic} {msg.payload}")
        try:
            payload = json.loads(msg.payload)
            component = payload.get("component", "")
            state = payload.get("state", "")
            command = payload.get("command", "")

            # Process trolley commands
            if component == "trolley":
                if state == "forward":
                    self.trolley.set_trolley_state(TrolleyMovement.FORWARD)
                elif state == "backward":
                    self.trolley.set_trolley_state(TrolleyMovement.BACKWARD)
                else:
                    self.trolley.set_trolley_state(TrolleyMovement.NEUTRAL)

                print(f"Trolley state updated: {state}")

            elif command == "increment_speed":
                self.trolley.increment_speed()
                print("Speed incremented.")

            elif command == "stop":
                self.trolley.stop()
                print("Trolley stopped.")

            elif command == "release_stop":
                self.trolley.emergency_stop = False
                self.trolley.speed = 0.2  # Reset speed to minimum
                print("Emergency stop released.")

            elif command == "emergency_stop":
                self.trolley.emergency_stop = True
                self.trolley.direction = TrolleyMovement.NEUTRAL
                print("Emergency stop activated.")

            else:
                print("Unknown command received.")

        except json.JSONDecodeError:
            print("Invalid message format. Could not parse JSON.")

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        """Callback for successful subscription to a topic."""
        print(f"Subscribed: mid={mid}, QoS={granted_qos}")

    def on_publish(self, client, userdata, mid, properties=None):
        """Callback for successful message publishing."""
        print(f"Message published: mid={mid}")

    # Main loop
    def main_loop(self):
        """Main loop to continuously update trolley position."""
        self.client.loop_start()
        last_update_time = time.time()

        try:
            while self.running:
                current_time = time.time()
                delta_time = current_time - last_update_time

                if not self.trolley.emergency_stop:
                    self.trolley.update_position(delta_time)

                last_update_time = current_time
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("Stopping Trolley Controller.")
            self.running = False
            self.client.loop_stop()


if __name__ == "__main__":
    controller = TrolleyController()
    controller.main_loop()
