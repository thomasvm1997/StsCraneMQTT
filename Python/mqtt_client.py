import pygame
import json
import paho.mqtt.client as paho
from paho import mqtt
import time

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
TOP_SECTION_HEIGHT = 300
BOTTOM_SECTION_HEIGHT = HEIGHT - TOP_SECTION_HEIGHT
TOP_RIGHT_WIDTH = WIDTH // 2
TOP_LEFT_WIDTH = WIDTH // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Font (gehalveerd)
FONT = pygame.font.Font(None, 18)

# Dot sizes
DOT_RADIUS = 5
LINE_THICKNESS = 2
LINE_FIXED_HEIGHT = 123

# MQTT topics
MQTT_TOPICS = [
    "/hub/gantry/handbrake/lock",
    "/hub/gantry/handbrake/release",
    "/hub/gantry/location",
    "/hub/hoist/location",
    "/hub/trolley/location",
    "/hub/spreader/status",
    "/hub/spreader/lock",
    "/hub/spreader/unlock",
]

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MQTT Data Viewer")

# Load and transform assets
STS_IMAGE = pygame.image.load("../assets/STS_side.png")
STS_IMAGE = pygame.transform.scale(STS_IMAGE, (TOP_LEFT_WIDTH, TOP_SECTION_HEIGHT))

STS_BACK_IMAGE = pygame.image.load("../assets/STS_back.png")
STS_BACK_IMAGE = pygame.transform.scale(STS_BACK_IMAGE, (90, 425))

SKY_BACKGROUND = pygame.image.load("../assets/sky_background1.jpeg")
SKY_BACKGROUND = pygame.transform.scale(SKY_BACKGROUND, (WIDTH, BOTTOM_SECTION_HEIGHT))  # Covers the full bottom width

SHIP_IMAGE = pygame.image.load("../assets/ship_side.png")
SHIP_IMAGE = pygame.transform.scale(SHIP_IMAGE, (WIDTH, BOTTOM_SECTION_HEIGHT))  # Covers the full bottom width
SHIP_IMAGE = pygame.transform.flip(SHIP_IMAGE, True, False)

# Initial dot positions
DOT_X = 300
DOT_Y = 200
BOTTOM_DOT_X = WIDTH // 2
BOTTOM_DOT_Y = HEIGHT - 100

# States
handbrake_locked = False
spreader_locked = False

# Data dictionary for MQTT messages
data_dict = {}

# MQTT callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker.")
        for topic in MQTT_TOPICS:
            client.subscribe(topic, qos=1)
        print("Subscribed to all topics.")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global DOT_X, BOTTOM_DOT_X, DOT_Y, BOTTOM_DOT_Y, handbrake_locked, spreader_locked
    try:
        payload = msg.payload.decode("utf-8")
        json_object = json.loads(payload)
        data_dict[msg.topic] = json_object

        # Handle different topics
        if msg.topic == "/hub/gantry/handbrake/lock":
            handbrake_locked = True
        elif msg.topic == "/hub/gantry/handbrake/release":
            handbrake_locked = False
        elif msg.topic == "/hub/gantry/location" and not handbrake_locked:
            BOTTOM_DOT_X = json_object.get("x", BOTTOM_DOT_X)
        elif msg.topic == "/hub/hoist/location":
            new_y = json_object.get("y", BOTTOM_DOT_Y)
            BOTTOM_DOT_Y = new_y
            DOT_Y = new_y
        elif msg.topic == "/hub/trolley/location":
            DOT_X = json_object.get("x", DOT_X)
        elif msg.topic == "/hub/spreader/lock":
            spreader_locked = True
        elif msg.topic == "/hub/spreader/unlock":
            spreader_locked = False

    except json.JSONDecodeError:
        data_dict[msg.topic] = msg.payload.decode("utf-8")

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

        # --- TOP LEFT SECTION ---
        screen.blit(SKY_BACKGROUND, (0, 0))
        screen.blit(STS_IMAGE, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, 0, TOP_LEFT_WIDTH, TOP_SECTION_HEIGHT), 2)
        
        # Tekenen van een lijn boven de kraan(breedte 70 meter)
        ship_width_line_start = (50, 20)
        ship_width_line_end = (TOP_LEFT_WIDTH - 50, 20)
        pygame.draw.line(screen, BLACK, ship_width_line_start, ship_width_line_end, 2)

        # Label '70 meter' boven de lijn
        ship_width_label = FONT.render("70 meter", True, BLACK)
        label_x = (ship_width_line_start[0] + ship_width_line_end[0]) // 2 - ship_width_label.get_width() // 2
        label_y = ship_width_line_start[1] - 20
        screen.blit(ship_width_label, (label_x, label_y))
        
        # Berekeningen voor de lijn in het blauwe vlak
        black_box_height = 40
        black_box_end_x = TOP_LEFT_WIDTH // 2  # Het zwarte vak neemt de eerste helft in beslag
        blue_line_start_x = black_box_end_x + ((TOP_LEFT_WIDTH - black_box_end_x) * 0.15)  
        blue_line_end_x = black_box_end_x + ((TOP_LEFT_WIDTH - black_box_end_x) * 0.95)  
        blue_line_y = TOP_SECTION_HEIGHT - 10 

        # Teken de lijn
        pygame.draw.line(screen, RED, (blue_line_start_x, blue_line_y), (blue_line_end_x, blue_line_y), 2)

        # Label '30 meter' bij de lijn
        blue_line_label = FONT.render("30 meter", True, RED)
        blue_label_x = (blue_line_start_x + blue_line_end_x) // 2 - blue_line_label.get_width() // 2
        blue_label_y = blue_line_y - 25  # Plaats de tekst boven de lijn
        screen.blit(blue_line_label, (blue_label_x, blue_label_y))
        
        # Nieuwe lijn van boven naar beneden aan de linkerzijde
        line_start_y = LINE_FIXED_HEIGHT
        line_end_y = TOP_SECTION_HEIGHT - 40
        pygame.draw.line(screen, RED, (10, line_start_y), (10, line_end_y), 2)
        
        # Voeg het label '60 meter' boven de lijn
        height_label = FONT.render("60 meter", True, RED)
        label_x = 10 + 10  
        label_y = line_start_y + line_end_y // 2  
        screen.blit(height_label, (label_x, label_y))

        # Dots and lines for top-left
        pygame.draw.circle(screen, GREEN if spreader_locked else RED, (DOT_X, DOT_Y), DOT_RADIUS)
        pygame.draw.line(screen, BLACK, (DOT_X, DOT_Y), (DOT_X, LINE_FIXED_HEIGHT), LINE_THICKNESS)

        # --- TOP RIGHT SECTION ---
        pygame.draw.rect(screen, BLACK, (TOP_LEFT_WIDTH, 0, TOP_RIGHT_WIDTH, TOP_SECTION_HEIGHT))
        y_offset = 10  # Start hoogte in de rechterbovenhoek

        # Display handbrake status
        handbrake_status = "Locked" if handbrake_locked else "Released"
        text_surface = FONT.render(f"Handbrake: {handbrake_status}", True, WHITE)
        screen.blit(text_surface, (TOP_LEFT_WIDTH + 10, y_offset))
        y_offset += 40

        # Display gantry location
        gantry_location = data_dict.get("/hub/gantry/location", {"x": "N/A"})
        text_surface = FONT.render(f"Gantry: {gantry_location}", True, WHITE)
        screen.blit(text_surface, (TOP_LEFT_WIDTH + 10, y_offset))
        y_offset += 40

        # Display trolley location
        trolley_location = data_dict.get("/hub/trolley/location", {"x": "N/A"})
        text_surface = FONT.render(f"Trolley: {trolley_location}", True, WHITE)
        screen.blit(text_surface, (TOP_LEFT_WIDTH + 10, y_offset))
        y_offset += 40

        # Display hoist location
        hoist_location = data_dict.get("/hub/hoist/location", {"y": "N/A"})
        text_surface = FONT.render(f"Hoist: {hoist_location}", True, WHITE)
        screen.blit(text_surface, (TOP_LEFT_WIDTH + 10, y_offset))
        y_offset += 40

        # Display spreader lock status
        spreader_status = "Locked" if spreader_locked else "Unlocked"
        text_surface = FONT.render(f"Spreader Lock: {spreader_status}", True, WHITE)
        screen.blit(text_surface, (TOP_LEFT_WIDTH + 10, y_offset))
        y_offset += 40


        # --- BOTTOM SECTION ---
        # Step 1: Render the sky background first
        screen.blit(SKY_BACKGROUND, (0, TOP_SECTION_HEIGHT))  # Start from the top section height

        # Step 2: Render the ship image on top of the sky background
        screen.blit(SHIP_IMAGE, (0, TOP_SECTION_HEIGHT))  # Ensure the ship image is positioned correctly

        # Step 3: Render the crane image (STS_BACK_IMAGE) over the ship image
        back_image_x = (WIDTH - STS_BACK_IMAGE.get_width()) // 2
        back_image_y = TOP_SECTION_HEIGHT + (BOTTOM_SECTION_HEIGHT - STS_BACK_IMAGE.get_height()) // 2 - 47
        screen.blit(STS_BACK_IMAGE, (back_image_x, back_image_y))

        # Step 4: Draw the black rectangle at the bottom
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - 30, WIDTH, 30))  # A rectangle covering the bottom 30px

        # Dots and lines for bottom section
        pygame.draw.circle(screen, RED, (BOTTOM_DOT_X, BOTTOM_DOT_Y), DOT_RADIUS)
        pygame.draw.line(screen, BLACK, (BOTTOM_DOT_X, BOTTOM_DOT_Y), (BOTTOM_DOT_X, TOP_SECTION_HEIGHT + 100), LINE_THICKNESS)

        pygame.display.flip()
        clock.tick(30)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    client.loop_stop()
    client.disconnect()
    pygame.quit()
