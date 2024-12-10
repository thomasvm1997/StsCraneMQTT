import json
import paho.mqtt.client as paho
from paho import mqtt
import pygame
from pygame.locals import *

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

# State variables
handbrake_locked = None
spreader_locked = None
emergency_button_pressed = None

# MQTT Topics
topics = [
    "/hub/gantry/handbrake/lock",
    "/hub/gantry/handbrake/release",
    "/hub/spreader/lock",
    "/hub/spreader/unlock",
    "/hub/emergency/button/press",
    "/hub/emergency/button/release",
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
    global handbrake_locked, spreader_locked, emergency_button_pressed

    payload = msg.payload.decode('utf-8')
    print(f"Client received message - Topic: {msg.topic}, Payload: {payload}")
    try:
        payload_data = json.loads(payload)
        value = payload_data.get("value", "")

        # Update state based on the topic
        if msg.topic == "/hub/gantry/handbrake/lock":
            handbrake_locked = True
        elif msg.topic == "/hub/gantry/handbrake/release":
            handbrake_locked = False
        elif msg.topic == "/hub/spreader/lock":
            spreader_locked = True
        elif msg.topic == "/hub/spreader/unlock":
            spreader_locked = False
        elif msg.topic == "/hub/emergency/button/press":
            emergency_button_pressed = True
        elif msg.topic == "/hub/emergency/button/release":
            emergency_button_pressed = False

    except json.JSONDecodeError:
        print(f"Invalid JSON payload received on topic {msg.topic}")

# Display message customization
def get_display_message():
    """Generate display messages for the state variables."""
    messages = []
    if handbrake_locked is not None:
        messages.append(f"Handbrake: {'Locked' if handbrake_locked else 'Unlocked'}")
    if spreader_locked is not None:
        messages.append(f"Spreader: {'Locked' if spreader_locked else 'Unlocked'}")
    if emergency_button_pressed is not None:
        messages.append(f"Emergency Button: {'Pressed' if emergency_button_pressed else 'Released'}")
    return messages

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

# Main loop
running = True
clock = pygame.time.Clock()

try:
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(BLACK)

        # Section 1: Display State Data
        section1_rect = pygame.Rect(0, 0, WIDTH // 3, HEIGHT)
        pygame.draw.rect(screen, BLACK, section1_rect)
        y_offset = 10
        messages = get_display_message()
        for message in messages:
            text_surface = FONT.render(message, True, WHITE)
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
