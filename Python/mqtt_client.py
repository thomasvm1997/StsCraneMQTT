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
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MQTT Data Viewer with Crane Views")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_BLUE = (173, 216, 230)  # Light blue color
FONT = pygame.font.Font(None, 24)

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
        "/hub/hoist/location": "Top",
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

# Display message customization
def get_display_message(topic, payload):
    """Generate user-friendly display messages based on topic and payload."""
    try:
        payload_data = json.loads(payload)
        value = payload_data.get("value", "")
        
        # Define custom messages for specific topics
        if topic == "/hub/gantry/handbrake/lock" and value == "Locked":
            return "Handbrake Locked"
        elif topic == "/hub/gantry/handbrake/release" and value == "Released":
            return "Handbrake Released"
        elif topic == "/hub/gantry/location":
            return f"Gantry Location: {value}"
        elif topic == "/hub/hoist/location":
            return f"Hoist Location: {value}"
        elif topic == "/hub/trolley/location":
            return f"Trolley Location: {value}"
        elif topic == "/hub/spreader/widen":
            return "Spreader Widening"
        elif topic == "/hub/spreader/narrow":
            return "Spreader Narrowing"
        elif topic == "/hub/spreader/lock":
            return "Spreader Locked"
        elif topic == "/hub/spreader/unlock":
            return "Spreader Unlocked"
        else:
            return f"{topic}: {value}"  # Default fallback

    except json.JSONDecodeError:
        return f"{topic}: {payload}"

# Draw STS Crane (placeholder graphics)
def draw_sts_crane_side_view(surface, x, y):
    pygame.draw.rect(surface, GRAY, (x, y, 200, 400))  # Crane base
    pygame.draw.line(surface, WHITE, (x+100, y), (x+100, y-100), 3)  # Hoist

def draw_sts_crane_rear_view(surface, x, y):
    pygame.draw.rect(surface, GRAY, (x, y, 400, 200))  # Rear crane base
    pygame.draw.line(surface, WHITE, (x+200, y), (x+200, y-100), 3)  # Hoist

# Initialize the MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)
client.username_pw_set("shark", "FishFish1")
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)
client.loop_start()

# Start mock data generation
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

        # Section 1: MQTT Data
        section1_rect = pygame.Rect(0, 0, WIDTH // 3, HEIGHT)
        pygame.draw.rect(screen, BLACK, section1_rect)
        y_offset = 10
        for topic, message in data_dict.items():
            display_message = get_display_message(topic, json.dumps(message))
            text_surface = FONT.render(display_message, True, WHITE)
            screen.blit(text_surface, (10, y_offset))
            y_offset += 30

        # Section 2: Side View of STS Crane (Light Blue Background)
        section2_rect = pygame.Rect(WIDTH // 3, 0, WIDTH // 3, HEIGHT)
        pygame.draw.rect(screen, LIGHT_BLUE, section2_rect)
        draw_sts_crane_side_view(screen, WIDTH // 3 + 50, HEIGHT // 2 - 200)

        # Section 3: Rear View of STS Crane (Light Blue Background)
        section3_rect = pygame.Rect(2 * WIDTH // 3, 0, WIDTH // 3, HEIGHT)
        pygame.draw.rect(screen, LIGHT_BLUE, section3_rect)
        draw_sts_crane_rear_view(screen, 2 * WIDTH // 3 + 50, HEIGHT // 2 - 100)

        pygame.display.flip()
        clock.tick(30)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()
    pygame.quit()
