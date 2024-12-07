import time
import json
import paho.mqtt.client as paho
from paho import mqtt
import pygame
from pygame.locals import *

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

# Callback for connection
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Client connected successfully to broker.")
        
        # Subscribe to required topics
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

# Main loop
running = True
clock = pygame.time.Clock()

try:
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        screen.fill(WHITE)
        y_offset = 10
        for topic, message in data_dict.items():
            text_surface = FONT.render(f"{topic}: {message}", True, BLACK)
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
