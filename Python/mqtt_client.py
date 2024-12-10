import pygame
import json
import paho.mqtt.client as paho
from paho import mqtt
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MQTT Data Viewer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
FONT = pygame.font.Font(None, 36)

# Load and scale the side image
sts_image = pygame.image.load("../assets/STS_side.png")  
sts_image = pygame.transform.scale(sts_image, (400, 300))

# Load and scale the back image
sts_back_image = pygame.image.load("../assets/STS_back.png")  
sts_back_image = pygame.transform.scale(sts_back_image, (95, 365))

# Initial dot position and line height
dot_x = 300
dot_y = 200
line_fixed_height = 123

# New dot for the bottom of the screen
bottom_dot_x = WIDTH // 2  # Horizontal center of the bottom screen
bottom_dot_y = HEIGHT - 20  # A bit above the bottom (in this case, 20 pixels above)

# Dictionary to hold incoming MQTT data
data_dict = {}

# List of MQTT topics to subscribe to
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

# MQTT client connection callback
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Client connected successfully to broker.")
        for topic in topics:
            client.subscribe(topic, qos=1)
        print("Client subscribed to all topics.")
    else:
        print(f"Failed to connect, return code {rc}")

# MQTT message callback
def on_message(client, userdata, msg):
    print(f"Client received message - Topic: {msg.topic}, Payload: {msg.payload.decode('utf-8')}")
    try:
        payload = msg.payload.decode('utf-8')
        json_object = json.loads(payload)
        data_dict[msg.topic] = json_object
    except json.JSONDecodeError:
        data_dict[msg.topic] = msg.payload.decode('utf-8')

# Initialize MQTT client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Assign MQTT callbacks
client.on_connect = on_connect
client.on_message = on_message

# Set TLS version for secure connection
client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)

# Set username and password for MQTT connection
client.username_pw_set("shark", "FishFish1")

# Connect to the MQTT broker
client.connect("4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud", 8883)

# Start MQTT network loop
client.loop_start()

running = True
clock = pygame.time.Clock()

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(LIGHT_BLUE)

        # Draw the side image in the top left area
        screen.blit(sts_image, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, 0, 400, 300), 2)

        # Draw the red dot at the top (first dot)
        pygame.draw.circle(screen, RED, (dot_x, dot_y), 5)  # Red dot
        pygame.draw.line(screen, BLACK, (dot_x, dot_y), (dot_x, line_fixed_height), 2)  # Line connected to fixed height

        # Draw the data area (black background for data display)
        pygame.draw.rect(screen, BLACK, (400, 0, 400, 300))  
        y_offset = 10
        for topic, message in data_dict.items():
            text_surface = FONT.render(f"{topic}: {message}", True, WHITE)
            screen.blit(text_surface, (410, y_offset))
            y_offset += 40

        # Draw the bottom boundary of the data area
        pygame.draw.rect(screen, WHITE, (0, 300, WIDTH, HEIGHT - 300), 2)

        # Draw the red dot at the bottom center
        pygame.draw.circle(screen, RED, (bottom_dot_x, bottom_dot_y), 5)  # Red dot

        # Draw a line from the bottom red dot to a fixed height
        pygame.draw.line(screen, BLACK, (bottom_dot_x, bottom_dot_y), (bottom_dot_x, 430), 2)  # Line to fixed height

        # Draw the STS_back image centered in the bottom rectangle, 10px higher (after drawing the line)
        back_image_x = (WIDTH - sts_back_image.get_width()) // 2  
        back_image_y = 300 + (HEIGHT - 300 - sts_back_image.get_height()) // 2 - 10  # Vertical center with 10px higher offset
        screen.blit(sts_back_image, (back_image_x, back_image_y))  # Draw image after the line to ensure it is on top

        # Draw the black field from the bottom to 10 pixels high (cover the full width)
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - 10, WIDTH, 10))

        pygame.display.flip()

        clock.tick(30)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Stop MQTT loop and disconnect before quitting
    client.loop_stop()
    client.disconnect()
    pygame.quit()
