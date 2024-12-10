import pygame
import json
import paho.mqtt.client as paho
from paho import mqtt
import time

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MQTT Data Viewer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
FONT = pygame.font.Font(None, 36)

# Load assets
sts_image = pygame.image.load("../assets/STS_side.png")
sts_image = pygame.transform.scale(sts_image, (400, 300))
sts_back_image = pygame.image.load("../assets/STS_back.png")
sts_back_image = pygame.transform.scale(sts_back_image, (90, 425))
sky_background = pygame.image.load("../assets/sky_background1.jpeg")
sky_background = pygame.transform.scale(sky_background, (400, 300))
ship_side = pygame.image.load("../assets/ship_side.png")
ship_side = pygame.transform.scale(ship_side, (800, 330))  # Ensure it covers the bottom width
ship_side = pygame.transform.flip(ship_side, True, False)
# Initial dot positions and line height
dot_x = 300
dot_y = 200
line_fixed_height = 123
bottom_dot_x = WIDTH // 2
bottom_dot_y = HEIGHT - 100

# Movement states
handbrake_locked = False
spreader_locked = False

# Data dictionary for MQTT messages
data_dict = {}

# Topics to subscribe to
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

# MQTT callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker.")
        for topic in topics:
            client.subscribe(topic, qos=1)
        print("Subscribed to all topics.")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global dot_x, bottom_dot_x, dot_y, bottom_dot_y, handbrake_locked, spreader_locked
    try:
        payload = msg.payload.decode('utf-8')
        json_object = json.loads(payload)
        data_dict[msg.topic] = json_object

        # Handle different topics
        if msg.topic == "/hub/gantry/handbrake/lock":
            handbrake_locked = True
        elif msg.topic == "/hub/gantry/handbrake/release":
            handbrake_locked = False
        elif msg.topic == "/hub/gantry/location" and not handbrake_locked:
            bottom_dot_x = json_object.get("x", bottom_dot_x)
        elif msg.topic == "/hub/hoist/location":
            new_y = json_object.get("y", bottom_dot_y)
            bottom_dot_y = new_y
            dot_y = new_y
        elif msg.topic == "/hub/trolley/location":
            dot_x = json_object.get("x", dot_x)
        elif msg.topic == "/hub/spreader/lock":
            spreader_locked = True
        elif msg.topic == "/hub/spreader/unlock":
            spreader_locked = False

    except json.JSONDecodeError:
        data_dict[msg.topic] = msg.payload.decode('utf-8')

# MQTT setup
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
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(LIGHT_BLUE)

        # Top section background
        screen.blit(sky_background, (0, 0))
        screen.blit(sts_image, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, 0, 400, 300), 2)

        # Top section dots and lines
        pygame.draw.circle(screen, GREEN if spreader_locked else RED, (dot_x, dot_y), 5)
        pygame.draw.line(screen, BLACK, (dot_x, dot_y), (dot_x, line_fixed_height), 2)
        pygame.draw.rect(screen, BLACK, (400, 0, 400, 300))
        y_offset = 10
        for topic, message in data_dict.items():
            text_surface = FONT.render(f"{topic}: {message}", True, WHITE)
            screen.blit(text_surface, (410, y_offset))
            y_offset += 40

        # Bottom section background
        screen.blit(ship_side, (0, 300))  # Place the ship image at the start of the bottom screen
        pygame.draw.rect(screen, WHITE, (0, 300, WIDTH, HEIGHT - 300), 2)

        # Bottom section dots and lines
        pygame.draw.circle(screen, RED, (bottom_dot_x, bottom_dot_y), 5)
        pygame.draw.line(screen, BLACK, (bottom_dot_x, bottom_dot_y), (bottom_dot_x, 400), 2)
        back_image_x = (WIDTH - sts_back_image.get_width()) // 2
        back_image_y = 300 + (HEIGHT - 300 - sts_back_image.get_height()) // 2 - 47
        screen.blit(sts_back_image, (back_image_x, back_image_y))
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - 30, WIDTH, 30))

        pygame.display.flip()
        clock.tick(30)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    client.loop_stop()
    client.disconnect()
    pygame.quit()
