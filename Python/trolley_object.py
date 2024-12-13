import pygame
import time

class Trolley:
    def __init__(self, x, y, width, height, min_x, max_x):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_x = min_x
        self.max_x = max_x
        self.speed = 0.2 #minimum speed
        self.emergency_stop = False
        self.last_update = time.time()
        self.last_message_time = time.time()

    def move(self, direction, delta_time):
        if self.emergency_stop:
            return
        distance = self.speed * direction * delta_time
        self.x += distance

        #trolley stays in boundaries
        if self.x < self.min_x:
            self.x = self.min_x
        elif self.x > self.max_x:
            self.x - self.max_x
    
    def increment_speed(self):
        if not self.emergency_stop:
            self.speed += 0.2  #increase speed by 0.2 m/s
            print(f"Speed increased to {self.speed} m/s")

    def reset_speed(self):
        self.speed = 0.2  #reset to minimum speed
        print("Speed reset to minimum (0.2 m/s)")

    def emergency_stop_action(self):
        self.emergency_stop = True
        self.speed = 0  #stop all movement
        print("Emergency stop activated")

    def release_emergency_stop(self):
        self.emergency_stop = False
        self.reset_speed()
        print("Emergency stop released")
    
    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
