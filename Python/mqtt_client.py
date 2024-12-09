import time
import json
import paho.mqtt.client as paho
from paho import mqtt
import pygame
from pygame.locals import *
from threading import Thread

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MQTT Data Viewer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Dictionary to store incoming data for display
data_dict = {}

# MQTT Topics
topics = [
    "/hub/gantry/handbrake/lock",
    "/hub/gantry/handbrake/release",
    "/hub/gantry/location",
    "/hub/hoist/location",
    "/hub/trolley/location",
    "/hub/spreader/widen",
    "/hub/spreader/narrow",
    "/hub/spreader/lock",
    "/hub/spreader/unlock"
]

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Client connected successfully to broker.")
        
        # Subscribe to required topics
        for topic in topics:
            client.subscribe(topic, qos=1)
        
        print("Client subscribed to all topics.")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback for receiving messages
def on_message(client, userdata, msg):
    print(f"Client received message - Topic: {msg.topic}, Payload: {msg.payload.decode('utf-8')}")
    try:
        payload = msg.payload.decode('utf-8')
        json_object = json.loads(payload)
        data_dict[msg.topic] = json_object
    except json.JSONDecodeError:
        data_dict[msg.topic] = msg.payload.decode('utf-8')

# Mock data generator
def mock_data_generator():
    mock_values = {
        "/hub/gantry/handbrake/lock": "Locked",
        "/hub/gantry/handbrake/release": "Released",
        "/hub/gantry/location": "East Section",
        "/hub/hoist/location": "top",
        "/hub/trolley/location": "Middle",
        "/hub/spreader/widen": "Widening",
        "/hub/spreader/narrow": "Narrowing",
        "/hub/spreader/lock": "Locked",
        "/hub/spreader/unlock": "Unlocked"
    }

    while True:
        for topic, value in mock_values.items():
            mock_message = json.dumps({"value": value, "timestamp": time.time()})
            on_message(client, None, type("MQTTMessage", (), {"topic": topic, "payload": mock_message.encode('utf-8')}))
            time.sleep(0.5)

# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

# Enable TLS for secure connection
client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)

# Set username and password for MQTT
client.username_pw_set("shark", "FishFish1")

# Connect to HiveMQ broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start the MQTT loop in the background
client.loop_start()

# Start the mock data generator in a separate thread
mock_thread = Thread(target=mock_data_generator, daemon=True)
mock_thread.start()

# Main loop
running = True
clock = pygame.time.Clock()

try:
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        screen.fill(BLACK)
        y_offset = 10
        for topic, message in data_dict.items():
            text_surface = FONT.render(f"{topic}: {message}", True, WHITE)
            screen.blit(text_surface, (10, y_offset))
            y_offset += 40

        pygame.display.flip()

        clock.tick(30)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()
    pygame.quit()
